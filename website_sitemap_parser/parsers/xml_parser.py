import logging
import requests
from lxml import etree
from gzip import GzipFile
from website_sitemap_parser.elements import NewsPage, Page, Sitemap, RootSitemap
from website_sitemap_parser.config import DEFAULT_COOKIES, DEFAULT_HEADERS, DEFAULT_TIMEOUT


def get_element_values(elem):
    if not len(elem):
        return {}

    values = {}
    for sub_elem in elem:
        if len(sub_elem):
            values["".join(sub_elem.tag.split('}')[1:])] = get_element_values(sub_elem)
        else:
            values["".join(sub_elem.tag.split('}')[1:])] = sub_elem.text
    return values


def parse(url, timeout=None, headers=None, cookies=None, include_root_sitemap=False):
    response = requests.get(
        url=url,
        headers=headers or DEFAULT_HEADERS,
        timeout=timeout or DEFAULT_TIMEOUT,
        cookies=cookies or DEFAULT_COOKIES,
        stream=True
    )
    if not response.ok:
        if response.status_code != 404:
            logging.warning(
                f'Failed to retrieve parse sitemap with error status {response.status_code} on url: {url}'
            )
        return []

    stream = response.raw

    # response.iter_content is actually better
    if response.headers.get('Content-Encoding') == 'gzip':
        stream = GzipFile(fileobj=stream)

    context = etree.iterparse(stream, events=('end',), tag=['{*}url', '{*}sitemap'])

    try:
        for action, elem in context:
            tag = "".join(elem.tag.split('}')[1:])

            values = get_element_values(elem)

            if not values.get('loc'):
                logging.warning(f'Missing location for element: {tag} {values}')
                continue

            if tag == 'url' and 'news' in values:
                news_values = values.get('news') or {}
                yield NewsPage(
                    url=values['loc'],
                    last_modified=values.get('lastmod'),
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
                    last_modified=values.get('lastmod'),
                    priority=values.get('priority'),
                    change_freq=values.get('changefreq')
                )
            elif tag == 'sitemap':
                yield Sitemap(
                    url=values['loc'],
                    last_modified=values.get('lastmod'),
                    priority=values.get('priority'),
                    change_freq=values.get('changefreq')
                )

            elem.clear()
            while elem.getprevious() is not None:
                if elem.getparent() is not None:
                    del elem.getparent()[0]
    except etree.XMLSyntaxError:
        logging.warning(f'Failed processing: {url}')
        return []

    if include_root_sitemap:
        yield RootSitemap(url=url)

    return []
