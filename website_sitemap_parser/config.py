
DEFAULT_TIMEOUT = 60
DEFAULT_READ_TIMEOUT = 60 * 4  # 4 minutes
DEFAULT_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:92.0) Gecko/20100101 Firefox/92.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'nl,en-US;q=0.7,en;q=0.3',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Cache-Control': 'max-age=0',
    'TE': 'trailers',
}

DEFAULT_COOKIES = {
    "consentUUID": "a469f52f-0654-4c08-9eaf-5b257e94eae3",
    "authId": "a469f52f-0654-4c08-9eaf-5b257e94eae3"
}
SITEMAP_CHECK_URLS = [
    "/sitemap.xml",
    "/sitemap-news.xml",
    "/sitemap_index.xml",
    "/sitemap_news.xml"
]
DEFAULT_DEPTH = 10
