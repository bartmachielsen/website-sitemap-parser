import logging
import requests
from lxml import etree
from gzip import GzipFile
from website_sitemap_parser.elements import NewsPage, Page, Sitemap, RootSitemap
from website_sitemap_parser.config import DEFAULT_COOKIES, DEFAULT_HEADERS, DEFAULT_TIMEOUT, DEFAULT_READ_TIMEOUT

from stopit import ThreadingTimeout as Timeout, TimeoutException
import dateparser


def get_element_values(elem):
    if not len(elem):
        return {}

    values = {}
    for sub_elem in elem:
        if callable(sub_elem.tag):
            continue

        if len(sub_elem):
            values["".join(sub_elem.tag.split('}')[1:])] = get_element_values(sub_elem)
        else:
            values["".join(sub_elem.tag.split('}')[1:])] = sub_elem.text
    return values


def parse(url, timeout=None, headers=None, cookies=None, include_root_sitemap=False):
    response = None
    try:
        with Timeout(timeout or DEFAULT_TIMEOUT):
            response = requests.get(
                url=url,
                headers=headers or DEFAULT_HEADERS,
                timeout=timeout or DEFAULT_TIMEOUT,
                cookies=cookies or DEFAULT_COOKIES,
                stream=True
            )
    except requests.exceptions.RequestException as request_exception:
        logging.warning(f'Failed to retrieve sitemap from url: {url} due to {request_exception}')
        return []
    except TimeoutException:
        logging.warning(f'Timeout exception: {url}')
        return []

    if not response or not response.ok:
        if response and response.status_code != 404:
            logging.warning(
                f'Failed to retrieve parse sitemap with error status {response.status_code} on url: {url}'
            )
        return []

    stream = response.raw

    if response.headers.get('Content-Type') == 'text/plain' or url.endswith('.txt'):
        for line in response.iter_lines():
            yield Page(url=line.decode('utf-8'))

        return []

    # response.iter_content is actually better
    if response.headers.get('Content-Encoding') == 'gzip' or \
            url.endswith('.gz') or \
            response.headers.get('content-type') == 'application/octet-stream':
        stream = GzipFile(fileobj=stream)

    context = etree.iterparse(stream, events=('end',), tag=['{*}url', '{*}sitemap'])

    try:
        with Timeout(DEFAULT_READ_TIMEOUT):
            for action, elem in context:
                tag = "".join(elem.tag.split('}')[1:])

                values = get_element_values(elem)

                try:
                    lastmod = dateparser.parse(values.get('lastmod')) if values.get('lastmod') else None
                except Exception as e:
                    logging.warning(f'Failed parsing date due to: {e}')
                    lastmod = None

                if not values.get('loc'):
                    logging.warning(f'Missing location for element: {tag} {values}')
                    continue

                if tag == 'url' and 'news' in values:
                    news_values = values.get('news') or {}
                    yield NewsPage(
                        url=values['loc'],
                        last_modified=lastmod,
                        priority=values.get('priority'),
                        change_freq=values.get('changefreq'),
                        publication_date=news_values.get('publication_date'),
                        title=news_values.get('title'),
                        keywords=news_values.get('keywords'),
                        genres=news_values.get('genres'),
                        # image=
                    )
                elif tag == 'url':
                    yield Page(
                        url=values['loc'],
                        last_modified=lastmod,
                        priority=values.get('priority'),
                        change_freq=values.get('changefreq')
                    )
                elif tag == 'sitemap':
                    yield Sitemap(
                        url=values['loc'],
                        last_modified=lastmod,
                        priority=values.get('priority'),
                        change_freq=values.get('changefreq')
                    )

                elem.clear()
                while elem.getprevious() is not None:
                    if elem.getparent() is not None:
                        del elem.getparent()[0]
    except etree.XMLSyntaxError as e:
        logging.warning(f'Failed processing: {url} due to {e}')
        return []
    except TimeoutException:
        logging.warning(f'Timeout exception: {url}')
        return []

    if include_root_sitemap:
        yield RootSitemap(url=url)

    return []


if __name__ == '__main__':
    print(list(parse('http://ipv4.download.thinkbroadband.com/1GB.zip')))