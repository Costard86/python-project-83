import validators
from urllib.parse import urlparse


def normalize(url):
    url_parts = urlparse(url.lower())
    if url_parts.scheme and url_parts.netloc:
        return f'{url_parts.scheme}://{url_parts.netloc}'
    return url


def validate(url):
    if url == '':
        return 'URL обязателен'
    if len(url) > 255:
        return 'URL не может превышать 255 символов'
    if not validators.url(url):
        return 'Некорректный URL'
