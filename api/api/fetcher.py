import logging

import validators
import requests
from bs4 import BeautifulSoup

from .utils import status
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
    if result.status_code != 200:
        return None, status.UNEXPECTED_SERVER_RESPONSE

    return result, status.OK


def get_soup_from_url(url):
    logger.debug("Fetching the url...")
    result, status = fetch_url(url)
    if not result:
        return None, status

    logger.debug("Generating soup object...")
    try:
        # soup converts to unicode by itself, passing content and input encoding
        soup = BeautifulSoup(result.content, 'lxml', from_encoding=result.encoding)
    except Exception as e:
        # bs4 doesn't specify the set of possible exceptions
        logger.debug("BeautifulSoup exception: {}".format(e))
        return None, status.HTML_DOM_PARSING_ERROR
    else:
        return soup, status.OK
