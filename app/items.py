# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field
from itemloaders.processors import TakeFirst


class Product(Item):
    name = Field(output_processor=TakeFirst())
    price = Field(output_processor=TakeFirst())
    images = Field()
    specs = Field(output_processor=TakeFirst())
    url = Field(output_processor=TakeFirst())
    availability = Field(output_processor=TakeFirst())
    lowest_stock = Field(output_processor=TakeFirst())