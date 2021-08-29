from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from app.spiders.ProductsSpider import ProductsSpider


def get_settings():
    settings = Settings()
    settings.set('FEED_URI', 'products.json')
    settings.set('FEED_FORMAT', 'json')
    settings.set('FEED_EXPORT_ENCODING', 'utf-8')

    return settings

# main driver
if __name__ == '__main__':
    # run spider
    process = CrawlerProcess(settings=get_settings())
    process.crawl(ProductsSpider)
    process.start()
