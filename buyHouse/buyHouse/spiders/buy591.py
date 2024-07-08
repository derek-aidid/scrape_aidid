from typing import Iterable

import scrapy
from scrapy import Request


# from quotes_js_scraper.items import QuoteItem


class Buy591Spider(scrapy.Spider):
    name = "buy591"

    def start_requests(self):
        url = "https://quotes.toscrape.com/js/"
        yield scrapy.Request(url, meta=dict(
            playwright=True,
            playwright_include_page=True,
            playwright_page_methods=[PageMethod('wait_for_selector', 'div.quote')],
            errback=self.errback,
        ))

    async def parse(self, response):
        page = response.meta["playwright_page"]
        await page.close()

        for quote in response.css('div.quote'):
            quote_item = QuoteItem()
            quote_item['text'] = quote.css('span.text::text').get()
            quote_item['author'] = quote.css('small.author::text').get()
            quote_item['tags'] = quote.css('div.tags a.tag::text').getall()
            yield quote_item

    async def errback(self, failure):
        page = failure.request.meta["playwright_page"]
        await page.close()
