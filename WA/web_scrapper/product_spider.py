import scrapy

class ProductSpider(scrapy.Spider):
    name = 'product_spider'
    start_urls = ['https://www.amazon.in/s?k=mobile&crid=305WQFAS7GI2J&sprefix=mobi%2Caps%2C348&ref=nb_sb_noss_2']

    def parse(self, response):
        # Extract all product links
        for product_link in response.css('a.rush-component::attr(href)').extract():
            yield scrapy.Request(product_link, callback=self.parse_product)

        # Follow pagination links
        next_page = response.css('a.s-pagination-item::attr(href)').get()
        if next_page:
            yield scrapy.Request(next_page, callback=self.parse)

    def parse_product(self, response):
        # Extract product details
        title = response.css('div.product-title-word-break::text').get()


        # Save extracted data in a dictionary
        product = {
            'title': title,
        }

        yield product