import scrapy
from urllib.parse import urljoin

custom_settings = {
    "FEED_FORMAT": "json",
    "FEED_URI": "quotes.json",
}


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = ["http://quotes.toscrape.com/page/1/"]

    def parse(self, response):
        for quote in response.css("div.quote"):
            text = quote.css("span.text::text").get().strip()
            author = quote.css("small::text").get().strip()
            tags = quote.css("div.tags a.tag::text").getall()

            yield {
                "text": text,
                "author": author,
                "tags": tags,
            }

        next_page = response.css("li.next a::attr(href)").get()
        if next_page:
            next_page_url = urljoin(response.url, next_page)
            yield scrapy.Request(url=next_page_url, callback=self.parse)
