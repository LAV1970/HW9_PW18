import scrapy
import json


class AuthorsSpider(scrapy.Spider):
    name = "authors"
    start_urls = ["http://quotes.toscrape.com/page/1/"]

    def parse(self, response):
        authors = []
        for author in response.css("div.author-details"):
            full_name = author.css("h3.author-title::text").get().strip()
            born_date = author.css("span.author-born-date::text").get().strip()
            born_location = author.css("span.author-born-location::text").get().strip()
            description = author.css("div.author-description::text").get().strip()

            authors.append(
                {
                    "full_name": full_name,
                    "born_date": born_date,
                    "born_location": born_location,
                    "description": description,
                }
            )

        with open("authors.json", "w") as authors_file:
            json.dump(authors, authors_file, indent=2)
