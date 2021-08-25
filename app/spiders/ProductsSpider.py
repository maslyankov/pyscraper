import scrapy
from scrapy.loader import ItemLoader
from re import sub

from app.items import Product


def strip_str(str):
    return sub(r"[\n\t\s]*", "", str)


def calc_specs(response):
    specs = dict()

    specs_selector = response.css('div.product-classifications table.table tbody tr')
    for row in specs_selector:
        item_name = row.xpath('td[1]//text()').extract_first()
        item_val = strip_str(row.xpath('td[2]//text()').extract_first())

        specs[item_name] = item_val

    return specs


class ProductsSpider(scrapy.Spider):
    name = "products"
    start_urls = [
        'https://mr-bricolage.bg/instrumenti/elektroprenosimi-instrumenti/vintoverti/c/006003013?q=%3Arelevance&page=0&priceValue=',
    ]

    def parse(self, response):
        page = response.url.split("page=")[-1].split("&price")[0]

        # Save parsed page to file (not required)
        # filename = f'products-{page}.html'
        # with open(filename, 'wb') as f:
        #     f.write(response.body)
        # self.log(f'Saved file {filename}')

        # Get products urls list
        prod_urls = response.css('div.product div.title a.name::attr(href)').getall()

        # Parse every product separately
        yield from response.follow_all(prod_urls, self.parse_product)

        # Iterate through all pages...
        is_last_page = response.xpath(
            "//li[contains(@class, 'pagination-next') and contains(@class, 'disabled')]").get()
        if not is_last_page:
            next_page = response.css('li.pagination-next a').attrib['href']
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)

    @staticmethod
    def parse_product(response):
        # Get product specs
        l = ItemLoader(item=Product(), response=response)
        l.add_css('name', 'h1.js-product-name::text')
        l.add_css('price', 'p.js-product-price::attr(data-price-value)')
        l.add_css('images', 'div.popup-gallery img::attr(src)')
        l.add_value('specs', calc_specs(response))

        return l.load_item()
