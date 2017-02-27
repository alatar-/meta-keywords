from bs4 import BeautifulSoup
import requests


def fetch_url(url):
    result = requests.get(url)

    return result


def get_url_soup(url):
    result = fetch_url(url)
    soup = BeautifulSoup(result.content, 'html.parser')

    return soup
