from urllib.parse import urlparse
import requests


def normalize_url(raw_url):
    parsed_url = urlparse(raw_url)
    normalized_url = f'{parsed_url.scheme}://{parsed_url.netloc}'
    return normalized_url

def fetch_and_parse_url(url):
    try:
        print(url)
        response = requests.get(url)
        response.raise_for_status()
        return {'status_code': response.status_code}
    except requests.RequestException:
        return {'error': 'Произошла ошибка при проверке'}