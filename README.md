# Website Sitemap Parser
Python package for scraping sitemaps of websites

## Getting Started

```pip install website-sitemap-parser```

```python
from website_sitemap_parser import search_sitemaps, process_sitemap

for page in search_sitemaps('https://www.nu.nl'):
    print(page)
```


## Future development
- implement exponential backoff on 429 requests
- delays between requests