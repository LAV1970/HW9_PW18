import scrapy
import json


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = ["http://quotes.toscrape.com/page/1/"]

    def parse(self, response):
        quotes = []
        for quote in response.css("div.quote"):
            tags = quote.css("div.tags a.tag::text").getall()
            author = quote.css("small::text").get().strip()
            text = quote.css("span.text::text").get().strip()

            quotes.append(
                {
                    "tags": tags,
                    "author": author,
                    "quote": text,
                }
            )

        next_page = response.css("li.next a::attr(href)").get()
        if next_page:
            yield scrapy.Request(url=next_page, callback=self.parse)

        with open("quotes.json", "w") as quotes_file:
            json.dump(quotes, quotes_file, indent=2)
