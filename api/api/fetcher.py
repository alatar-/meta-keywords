import logging

import validators
import requests
from bs4 import BeautifulSoup

from .utils import status
from . import config

logger = logging.getLogger("main")


def fetch_url(url):
    logger.debug("Preprocessing and validating provided url:", url)
    url = url.lstrip(':/')
    if not url.startswith('http'):
        url = 'http://' + url
    if not validators.url(url, public=True):
        return None, status.URL_VALIDATION_FAILED

    logger.debug("Requesting resource:", url)
    try:
        result = requests.get(url, headers={'Accept': 'text/html'}, timeout=config.FETCHER_TIMEOUT, allow_redirects=True)
    except requests.exceptions.InvalidURL:
        return None, status.URL_VALIDATION_FAILED
    except requests.exceptions.RequestException:
        return None, status.FETCHING_OR_DECODING_ERROR

    logger.debug("Decoding the response (code %d)..." % result.status_code)
    if result.status_code != 200:
        return None, status.UNEXPECTED_SERVER_RESPONSE

    unicoded_result = result.text
    return unicoded_result, status.OK


def get_soup_from_url(url):
    logger.debug("Fetching the url...")
    result, status = fetch_url(url)
    if not result:
        return None, status

    logger.debug("Generating soup object...")
    try:
        soup = BeautifulSoup(result, 'lxml')
    except:
        return None, status.HTML_DOM_PARSING_ERROR
    else:
        return soup, status.OK
