import scrapy


class AuthorsSpider(scrapy.Spider):
    name = 'authors'
    
    def start_requests(self):
        return super().start_requests()