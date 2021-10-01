from typing import List

from website_sitemap_parser.parsers import robots_parser, xml_parser
from website_sitemap_parser.config import SITEMAP_CHECK_URLS
from website_sitemap_parser.elements import Page, Sitemap
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
            sitemap,
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


if __name__ == '__main__':
    for page in search_sitemaps('https://www.ed.nl'):
        print(page)