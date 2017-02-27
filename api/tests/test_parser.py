import mock

from api import parser


def load_html_fixture(filename):
    with open("tests/fixtures/%s" % filename, 'r') as f:
        content = "".join(f.readlines())
        return BeautifulSoup(content, 'html.parser').find()


class TestParser:
    def test_test(self):
        assert 'expected' == 'expected'
