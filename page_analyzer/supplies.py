from urllib.parse import urlparse


def normalize_url(raw_url):
    parsed_url = urlparse(raw_url)
    normalized_url = f'{parsed_url.scheme}://{parsed_url.netloc}'
    return normalized_url