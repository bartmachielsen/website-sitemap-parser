import requests
import logging
from urllib.parse import urlparse, urlunparse
from website_sitemap_parser.config import DEFAULT_COOKIES, DEFAULT_HEADERS, DEFAULT_TIMEOUT


def get_robots_url(url):
    parsed_url = urlparse(url)
    return urlunparse((
        parsed_url.scheme,
        parsed_url.netloc,
        '/robots.txt',  # path
        '',  # params
        '',  # query
        '',  # fragment
    ))


def parse_robots(url, timeout=None, headers=None, cookies=None):
    response = requests.get(
        url=get_robots_url(url),
        headers=headers or DEFAULT_HEADERS,
        timeout=timeout or DEFAULT_TIMEOUT,
        cookies=cookies or DEFAULT_COOKIES,
        stream=True
    )
    if not response.ok:
        if response.status_code != 404:
            logging.warning(
                f'Failed to retrieve parse robots.txt with error status {response.status_code} on url: {url}'
            )
        return []

    sitemaps = []
    for line in response.iter_lines():
        line = line.strip().decode('utf-8')
        if not line or line[0] == "#" or not line.lower().startswith('sitemap:'):
            continue

        sitemaps.append(line.split(': ')[1])
    return list(set(sitemaps))
