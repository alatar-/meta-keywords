import logging

import validators
import requests
from bs4 import BeautifulSoup

from .messages import status
from . import config

logger = logging.getLogger("main")


def fetch_url(url):
    logger.debug("Preprocessing and validating provided url: {url}".format(url=url))
    url = url.lstrip(':/')
    if not url.startswith('http'):
        url = 'http://' + url
    if not validators.url(url, public=True):
        return None, status.URL_VALIDATION_FAILED

    logger.debug("Requesting resource: {url}".format(url=url))
    try:
        result = requests.get(url, headers={'Accept': 'text/html'}, timeout=config.FETCHER_TIMEOUT, allow_redirects=True)
    except requests.exceptions.InvalidURL as e:
        logger.debug("InvalidURL Exception during request: {}".format(e))
        return None, status.URL_VALIDATION_FAILED
    except requests.exceptions.RequestException as e:
        logger.debug("Exception during request: {}".format(e))
        return None, status.FETCHING_OR_DECODING_ERROR

    logger.debug("Decoding the response (code {:d})...".format(result.status_code))

    switch = {
        200: status.OK,
        404: status.URL_NOT_FOUND,
    }
    req_status = switch.get(result.status_code, status.UNEXPECTED_SERVER_RESPONSE)
    return result, req_status


def get_soup_from_url(url):
    '''
    Generate HTML page tree object (soup) using BeautifulSoup lib.
    '''
    logger.debug("Fetching the url...")
    result, req_status = fetch_url(url)
    if req_status != status.OK:
        return None, req_status

    logger.debug("Generating soup object...")
    try:
        # soup converts to unicode by itself, passing content and input encoding
        soup = BeautifulSoup(result.content, 'lxml', from_encoding=result.encoding)
    except Exception as e:
        logger.warning("BeautifulSoup exception: {}".format(e))
        return None, status.HTML_DOM_PARSING_ERROR
    else:
        return soup, status.OK
