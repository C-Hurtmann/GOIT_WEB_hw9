from scrapy import Spider, Request
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from queue import Queue


class QuotessSpider(Spider):
    name = 'quotes'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['https://quotes.toscrape.com/']
    page = 0
    queue = Queue()
    

    def parse(self, response):
        self.page += 1
        quotes = response.xpath("//div[@class='quote']")
        for quote in quotes:
            quote_text = quote.xpath("span[@class='text']/text()").get()
            author = quote.xpath("span/small/text()").get()
            tags = quote.xpath("div/a/text()").getall()
            yield {'tags': tags, 'author': author, 'quote': quote_text}
            author_page = quote.xpath("span/a/@href").get()
            self.queue.put(self.start_urls[0] + author_page[1:])

        while not self.queue.empty():
            link = self.queue.get()
            yield Request(url=link, callback=self.parse_authors)
    
        print(str(self.page) + '-' * 80)
        next_page = response.xpath("//nav/ul/li[@class='next']/a/@href").get()
        if next_page:
            yield Request(url=self.start_urls[0] + next_page, callback=self.parse)

    def parse_authors(self, response):
        details = response.xpath("//div/div[@class='author-details']")
        author = details.xpath("h3/text()").get()
        born_date, born_location = details.xpath("p/span/text()").getall()
        description = details.xpath("div[@class='author-description']/text()").get()
        yield {'author': author, 'born_date': born_date, 'born_location': born_location, 'description': description}


if __name__ == '__main__':
    process = CrawlerProcess(get_project_settings())
    process.crawl(QuotessSpider)
    process.start()