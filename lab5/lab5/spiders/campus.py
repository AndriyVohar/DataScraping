import scrapy
from lab5.SeleniumRequest import SeleniumRequest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions 
# from selenium.webdriver import Chrome

# driver = Chrome(executable_path='../chromedriver.exe')

from lab5.items import Lab5Item


class CampusSpider(scrapy.Spider):
    name = "campus"
    allowed_domains = [""]
    start_urls = ["http://localhost:8080/posts"]

    def start_requests(self):   
        for url in self.start_urls:
            yield SeleniumRequest(
                url=url,
                callback=self.parse,
                wait_time=10,
                wait_until=expected_conditions.element_to_be_clickable(
                   (By.CSS_SELECTOR,
                    "page")
                ),
            )

    def parse(self, response):
        for img in response.css("div.post img"):
            url = img.css('::attr(src)').get()
            yield Lab5Item(
                url=url,
                image_urls=[url],
            )
