
class Page:
    def __init__(self, url, last_modified=None, priority=None, change_freq=None):
        self.url = url
        self.last_modified = last_modified
        self.priority = priority
        self.change_freq = change_freq

    def __repr__(self):
        return f"{self.__class__.__name__}(url=\"{self.url}\")"


class Sitemap(Page):
    pass


class RootSitemap(Sitemap):
    pass


class NewsPage(Page):
    def __init__(self, url, last_modified=None, priority=None, change_freq=None, publication_date=None, title=None, keywords=None, genres=None):
        super().__init__(url, last_modified, priority, change_freq)
        self.publication_date = publication_date
        self.title = title
        self.keywords = keywords
        self.genres = genres

    def __repr__(self):
        if self.title:
            return f"{self.__class__.__name__}(url=\"{self.url}\", title=\"{self.title}\")"
        return super().__repr__()