# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from mkr1.items import HeadphoneCategory, HeadphoneItem, ShopItem
import mysql.connector

class Mkr1Pipeline:
    def open_spider(self, spider):
        self.connection = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="",
            database="scrapy_mkr1_vohar"
        )
        self.cursor = self.connection.cursor()
        spider.logger.info("Connected to MySQL")
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS 
        headphone_categories (
            id INT AUTO_INCREMENT,
            PRIMARY KEY (id),
            name VARCHAR(70) NOT NULL,
            url VARCHAR(500)
        )""")
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS 
        headphone_items (
            id INT AUTO_INCREMENT,
            PRIMARY KEY (id),
            name VARCHAR(100) NOT NULL,
            category VARCHAR(70) NOT NULL,
            url VARCHAR(500)
        )""")
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS 
        shop_items (
            id INT AUTO_INCREMENT,
            PRIMARY KEY (id),
            name VARCHAR(70) NOT NULL,
            price VARCHAR(70) NOT NULL,
            headphone VARCHAR(70) NOT NULL
        )""")
        spider.logger.info("DB is ready ")
    
    def close_spider(self, spider):
        self.connection.close()
        spider.logger.info("Disconnected from MySQL ")

    def process_item(self, item, spider):
        if isinstance(item, HeadphoneCategory):
            self.cursor.execute(
                "INSERT INTO headphone_categories (name, url) VALUES (%s, %s);",
                [item.get("name"), item.get("url")])
        if isinstance(item, HeadphoneItem):
            self.cursor.execute(
                "INSERT INTO headphone_items (name, category, url) VALUES (%s, %s, %s);",
                [item.get("name"), item.get('category'), item.get("url")])
        if isinstance(item, ShopItem):
            self.cursor.execute(
                "INSERT INTO shop_items (name,price,headphone) VALUES (%s, %s, %s);",
                [item.get("name"), item.get('price'), item.get("headphone")])
        self.connection.commit()
        return item
