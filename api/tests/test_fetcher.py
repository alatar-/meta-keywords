from unittest.mock import MagicMock

from bs4 import BeautifulSoup

from api import fetcher
from api.utils import status


def load_file_content(filename):
    with open("tests/fixtures/%s" % filename, 'r') as f:
        content = "".join(f.readlines())
        return content


class TestFetchUrl:

    def test_invalid_url(self):
        assert (None, status.URL_VALIDATION_FAILED) == fetcher.fetch_url("afdfsfd")
        assert (None, status.URL_VALIDATION_FAILED) == fetcher.fetch_url("http:/adsf")
        assert (None, status.URL_VALIDATION_FAILED) == fetcher.fetch_url("ftp://asdfaafs")
        assert (None, status.URL_VALIDATION_FAILED) == fetcher.fetch_url("localhost/asddf")
        assert (None, status.URL_VALIDATION_FAILED) == fetcher.fetch_url("192.168.0.1/asd")

    def test_valid_url_response_different_than_http_200(self):
        mock_response = MagicMock(status_code=201, text=load_file_content('six_keywords_one_match.html'))
        fetcher.requests.get = MagicMock(return_value=mock_response)

        result, result_status = fetcher.fetch_url("http://www.correct.url.com/resource?param=213&")
        assert result is None
        assert status.UNEXPECTED_SERVER_RESPONSE == result_status


    def test_valid_url(self):
        mock_response = MagicMock(status_code=200, text=load_file_content('six_keywords_one_match.html'))
        fetcher.requests.get = MagicMock(return_value=mock_response)

        result, result_status = fetcher.fetch_url("http://www.correct.url.com/resource?param=213&")
        assert result is not None
        assert status.OK == result_status

class TestGetSoupFromUrl:

    def test_invlaid_input_html(self):
        mock_response = MagicMock(status_code=200, text=load_file_content('invalid_document.html'))
        fetcher.requests.get = MagicMock(return_value=mock_response)

        soup, result_status = fetcher.get_soup_from_url("http://www.correct.url")
        # input invalid but parser apparently still manages to parse it somehow
        assert soup is not None
        assert status.OK == result_status

    def test_valid_input(self):
        mock_response = MagicMock(status_code=200, text=load_file_content('meta_keywords_missing.html'))
        fetcher.requests.get = MagicMock(return_value=mock_response)

        soup, result_status = fetcher.get_soup_from_url("http://www.correct.url")
        assert status.OK == result_status
        assert isinstance(soup, BeautifulSoup)

