import re
import logging

logger = logging.getLogger("main")


def find_meta_keywords(soup):
    try:
        soup_keywords_tag = soup.find('head').find(attrs={"name": "keywords"})
        raw_keywords = soup_keywords_tag.get("content", "")
    except AttributeError:
        logger.debug('keywords meta tag missing or unvalid structure!')
        return []
    else:
        logger.debug('raw_keywords: {keywords}'.format(keywords=raw_keywords))
        keywords = map(lambda x: x.strip().lower(), raw_keywords.split(","))  # strip extra spacer, lowercase
        non_empty_keywords = filter(None, keywords)  # remove empty keywords
        unique_keywords = list(set(non_empty_keywords))  # remove duplicates
        logger.debug('unique_keywords: {keywords}'.format(keywords=unique_keywords))

        return unique_keywords


def count_keywords_in_text(soup, keywords):
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
    
    text_soup = soup.findAll(text=True)
    visible_text = "\n".join(filter(visibility_filter, text_soup))

    result = {}
    for key in keywords:
        # use some tokenizer for better results
        result[key] = visible_text.count(key)

    logger.debug("count_keywords result: {result}".format(result=result))
    return result
