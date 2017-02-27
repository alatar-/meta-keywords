import re


def visibility_filter(element):
    '''
    Helper filter to find only visible text from HTML page.

    Source: http://stackoverflow.com/a/1983219
    '''
    if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
        return False
    elif re.match('<!--.*-->', str(element)):
        return False
    return True


def count_keywords(soup):
    keywords = soup.find('head').find(attrs={"name": "keywords"})['content'].split(",")

    text = soup.findAll(text=True)
    visible_text = filter(visibility_filter, text)

    return keywords
