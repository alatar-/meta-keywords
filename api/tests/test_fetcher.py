from unittest.mock import MagicMock

from bs4 import BeautifulSoup

from api import fetcher
from api.messages import status


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

    def test_valid_url_unexpected_server_response(self):
        mock_response = MagicMock(status_code=201)
        fetcher.requests.get = MagicMock(return_value=mock_response)

        _, req_status = fetcher.fetch_url("http://www.correct.url.com/resource?param=213&")
        assert status.UNEXPECTED_SERVER_RESPONSE == req_status

    def test_valid_url_response_404_not_found(self):
        mock_response = MagicMock(status_code=404)
        fetcher.requests.get = MagicMock(return_value=mock_response)

        _, req_status = fetcher.fetch_url("http://www.correct.url.com/resource?param=213&")
        assert status.URL_NOT_FOUND == req_status


    def test_valid_url_response_200_ok(self):
        mock_response = MagicMock(status_code=200, content=load_file_content('six_keywords_one_match.html'))
        fetcher.requests.get = MagicMock(return_value=mock_response)

        soup, req_status = fetcher.fetch_url("http://www.correct.url.com/resource?param=213&")
        assert soup.content is not None
        assert status.OK == req_status

class TestGetSoupFromUrl:

    def test_invalid_input_html(self):
        mock_response = MagicMock(status_code=200, content=load_file_content('invalid_document.html'))
        fetcher.requests.get = MagicMock(return_value=mock_response)

        soup, req_status = fetcher.get_soup_from_url("http://www.correct.url")
        # input invalid but parser apparently still manages to parse it somehow
        assert soup is not None
        assert status.OK == req_status

    def test_valid_input(self):
        mock_response = MagicMock(status_code=200, content=load_file_content('six_keywords_one_match.html'))
        fetcher.requests.get = MagicMock(return_value=mock_response)

        soup, req_status = fetcher.get_soup_from_url("http://www.correct.url")
        assert status.OK == req_status
        assert isinstance(soup, BeautifulSoup)

