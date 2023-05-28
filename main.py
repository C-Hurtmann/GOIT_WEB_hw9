from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from database.connection import connect
from database.models import Quotes, Authors
from scraper.main.main.spiders.quotes import QuotessSpider


def main():
    process = CrawlerProcess(get_project_settings())
    process.crawl(QuotessSpider)
    process.start()


if __name__ == "__main__":
    main()

