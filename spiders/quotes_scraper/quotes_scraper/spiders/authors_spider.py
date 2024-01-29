import scrapy
import json
from urllib.parse import urljoin  # Add this import


class AuthorsSpider(scrapy.Spider):
    name = "authors"
    start_urls = ["http://quotes.toscrape.com/page/1/"]

    def parse(self, response):
        authors = []

        for quote in response.css("div.quote"):
            author = quote.css("small::text").get().strip()
            born_date_location = quote.css("span small::text").get().strip()

            # Handle missing description
            description = quote.css("span span[class='text']::text").get()
            description = description.strip() if description else None

            authors.append(
                {
                    "fullname": author,
                    "born_date_location": born_date_location,
                    "description": description,
                }
            )

        next_page = response.css("li.next a::attr(href)").get()
        if next_page:
            next_page_url = urljoin(
                response.url, next_page
            )  # Construct the complete URL
            yield scrapy.Request(url=next_page_url, callback=self.parse)

        with open("authors.json", "w") as authors_file:
            json.dump(authors, authors_file, indent=2)
