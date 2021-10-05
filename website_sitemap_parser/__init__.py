from typing import List

from website_sitemap_parser.parsers import robots_parser, xml_parser
from website_sitemap_parser.config import SITEMAP_CHECK_URLS
from website_sitemap_parser.elements import Page, Sitemap, RootSitemap
from urllib.parse import urljoin


def process_sitemap(url: str, timeout=None, headers=None, cookies=None):
    yield from xml_parser.parse(
        url,
        timeout=timeout,
        headers=headers,
        cookies=cookies,
        include_root_sitemap=False
    )


def search_sitemaps(url: str, timeout=None, headers=None, cookies=None) -> List[Page]:
    robots_txt_sitemaps = robots_parser.parse_robots(
        url,
        timeout=timeout,
        headers=headers,
        cookies=cookies
    )

    for sitemap in robots_txt_sitemaps:
        yield from xml_parser.parse(
            urljoin(url, sitemap),
            timeout=timeout,
            headers=headers,
            cookies=cookies,
            include_root_sitemap=True
        )

    for sitemap in SITEMAP_CHECK_URLS:
        yield from xml_parser.parse(
            urljoin(url, sitemap),
            timeout=timeout,
            headers=headers,
            cookies=cookies,
            include_root_sitemap=True
        )


def process_sitemap_recursive_pages(url: str, timeout=None, headers=None, cookies=None, max_depth=9) -> List[Page]:
    for page in process_sitemap(url, timeout, headers, cookies):
        if isinstance(page, Sitemap) and not isinstance(page, RootSitemap) and max_depth > 0:
            yield from process_sitemap_recursive_pages(page.url, timeout, headers, cookies, max_depth=max_depth-1)

        if not isinstance(page, Sitemap):
            yield page


def search_all_pages(url: str, timeout=None, headers=None, cookies=None) -> List[Page]:
    for sitemap in search_sitemaps(url, timeout, headers, cookies):
        if isinstance(sitemap, Sitemap) and not isinstance(sitemap, RootSitemap):
            yield from process_sitemap_recursive_pages(sitemap.url, timeout, headers, cookies)

        if not isinstance(sitemap, Sitemap):
            yield sitemap


if __name__ == '__main__':
    for _page in search_all_pages('https://www.michigansthumb.com'):
        print(_page)
