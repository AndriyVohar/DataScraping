import scrapy
from mkr1.items import HeadphoneCategory, HeadphoneItem, ShopItem

class HotlineSpider(scrapy.Spider):
    name = "hotline"
    allowed_domains = ["hotline.ua"]
    start_urls = ["https://hotline.ua/ua/av/"]

    def parse(self, response):
        headphone_categories = response.css('div[id="headphones"] + div a')
        for headphone_category in headphone_categories:
            link_to_next = headphone_category.css('::attr(href)').get()
            link_to_next = f"https://hotline.ua{link_to_next}"
            headphone_category_name = headphone_category.css('div::text').get()
            yield HeadphoneCategory(
                name = headphone_category_name,
                url = link_to_next,
            )
            yield scrapy.Request(
                url = link_to_next,
                callback= self.parse_headphones,
                meta={
                    "category": headphone_category_name,
                }
            )
    
    def parse_headphones(self,response):
        headphone_as = response.css('div.list-item a.item-title')
        for headphone_a in headphone_as:
            headphone_name = headphone_a.css('::text').get()
            headphone_link = headphone_a.css('::attr(href)').get()
            headphone_link = f"https://hotline.ua{headphone_link}"
            yield HeadphoneItem(
                name = headphone_name,
                url = headphone_link,
                category = response.meta.get('category')
            )
            yield scrapy.Request(
                url = headphone_link,
                callback= self.shops_parse,
                meta={
                    "headphone_name": headphone_name
                }
            )

    def shops_parse(self,response):
        shop_items = response.css('div.list__item')
        for shop_item in shop_items:
            # print(shop_item)
            shop_name = shop_item.css('a.shop__title::text').get()
            shop_price = shop_item.css('span.price__value::text').get()
            yield ShopItem(
                name = shop_name,
                price = shop_price,
                headphone = response.meta.get('headphone_name')
            )