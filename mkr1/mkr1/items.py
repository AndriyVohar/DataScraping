# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class HeadphoneCategory(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    url = scrapy.Field()

class HeadphoneItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    url = scrapy.Field()
    category = scrapy.Field()

class ShopItem(scrapy.Item):
    name = scrapy.Field()
    price = scrapy.Field()
    headphone = scrapy.Field()
    
