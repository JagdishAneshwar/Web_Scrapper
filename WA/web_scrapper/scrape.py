import scrapy

class ProductSpider(scrapy.Spider):
    name = 'product_spider'
    start_urls = ['https://www.flipkart.com/search?q=mobile&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off']

    def parse(self, response):
        # Extract all product links
        for product_link in response.css('a._1fQZEK::attr(href)').extract():
            yield scrapy.Request(product_link, callback=self.parse_product)

        # Follow pagination links
        next_page = response.css('a.ge-49M::attr(href)').get()
        if next_page:
            yield scrapy.Request(next_page, callback=self.parse)

    def parse_product(self, response):
        # Extract product details
        title = response.css('span.B_NuCI::text').get()
        price = response.css('div._30jeq3 ::text').get()

        # Save extracted data in a dictionary
        product = {
            'title': title,
            'price': price,
        }

        yield product