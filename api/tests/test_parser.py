from bs4 import BeautifulSoup

from api import parser


def get_soup_from_fixture(filename):
    with open("tests/fixtures/%s" % filename, 'r') as f:
        content = "".join(f.readlines())
        return BeautifulSoup(content, 'lxml')


class TestFindMetaKeywords:

    def test_meta_tag_missing(self):
        soup = get_soup_from_fixture('meta_keywords_missing.html')

        keywords = parser.find_meta_keywords(soup)
        assert type(keywords) is list
        assert not keywords

    def test_head_tag_missing(self):
        soup = get_soup_from_fixture('head_tag_missing.html')

        keywords = parser.find_meta_keywords(soup)
        assert type(keywords) is list
        assert not keywords

    def test_meta_keywords_valid(self):
        soup = get_soup_from_fixture('six_keywords_one_match.html')
        expected_keywords = ['automated notifications', 'voice api', 'call tracking', 'cloud communications', 'telephony infrastructure', 'sms api']

        keywords = parser.find_meta_keywords(soup)
        assert type(keywords) is list
        assert 6 == len(keywords)
        assert set(expected_keywords) == set(keywords)

    def test_meta_having_empty_keywords(self):
        soup = get_soup_from_fixture('basic_having_empty_keywords.html')
        expected_keywords = ['key4', 'keyword1', 'key2']

        keywords = parser.find_meta_keywords(soup)
        assert type(keywords) is list
        assert 3 == len(keywords)
        assert set(expected_keywords) == set(keywords)


class TestCountKeywordsInText:

    def test_count_keywords(self):
        keywords = ['automated notifications', 'voice api', 'call tracking', 'cloud communications', 'telephony infrastructure', 'sms api']
        soup = get_soup_from_fixture('six_keywords_one_match.html')
        expected_result = {
            'automated notifications': 0,
            'voice api': 0,
            'call tracking': 0,
            'cloud communications': 1,
            'telephony infrastructure': 0,
            'sms api': 0,
        }

        result = parser.count_keywords_in_text(soup, keywords)
        assert expected_result == result
