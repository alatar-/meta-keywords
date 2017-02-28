import validators
import pytest

from api import fetcher
from api.utils import status


class TestFetchUrl:

    def test_invalid_url(self):
        assert (None, status.URL_VALIDATION_FAILED) == fetcher.fetch_url("afdfsfd")
        assert (None, status.URL_VALIDATION_FAILED) == fetcher.fetch_url("http:/adsf")
        assert (None, status.URL_VALIDATION_FAILED) == fetcher.fetch_url("ftp://asdfaafs")
        assert (None, status.URL_VALIDATION_FAILED) == fetcher.fetch_url("localhost/asddf")
        assert (None, status.URL_VALIDATION_FAILED) == fetcher.fetch_url("192.168.0.1/asd")
