from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup


def normalize_url(raw_url):
    parsed_url = urlparse(raw_url)
    normalized_url = f'{parsed_url.scheme}://{parsed_url.netloc}'
    return normalized_url


def fetch_and_parse_url(url):
    try:
        print(url)
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        return {
            'title': soup.find('title').text if soup.find('title') else None,
            'h1': soup.find('h1').text if soup.find('h1') else None,
            'description': soup.find('meta', attrs={'name': 'description'})['content'] if soup.find('meta', attrs={'name': 'description'}) else None,  # noqa: E501
            'status_code': response.status_code
        }
    except requests.RequestException:
        return {'error': 'Произошла ошибка при проверке'}