# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from re import search
from scrapy.exceptions import DropItem
from lab2.items import StaffItem, DepartmentItem, FacultyItem
import mysql.connector

class Lab2Pipeline:
    def process_item(self, item, spider):
        if isinstance(item,FacultyItem):
            name = item.get('name')
            words = name.split()
            name = ' '.join(word.capitalize() for word in words)
            item['name'] = name
            return item
        if isinstance(item, DepartmentItem):
            faculty = item.get('faculty')
            words = faculty.split()
            faculty = ' '.join(word.capitalize() for word in words)
            item['faculty'] = faculty
            return item
        if isinstance(item, StaffItem):
            head_of_department = item.get('head_of_department')
            address = item.get('address')
            res = search(
                r"[А-ЯІЇЄ][а-яіїє\']+\s[А-ЯІЇЄ][а-яіїє\']+\s[А-ЯІЇЄ][а-яіїє\']+",
                head_of_department
            )
            if not res:
                res = search(
                    r"[А-ЯІЇЄ][а-яіїє\']+\s[А-ЯІЇЄ]\.\s?[А-ЯІЇЄ]\.",
                    name
                )
            if not res:
                raise DropItem(f"Bad name {name}")
            address = address.replace("\xa0", "")
            item['head_of_department'] = res.group(0)
            item['address'] = address
            return item

class MySqlPipeline:
    def open_spider(self, spider):
        self.connection = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="",
            database="scrapy_lab3"
        )
        self.cursor = self.connection.cursor()
        spider.logger.info("Connected to MySQL")
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS 
        faculty_items (
            id INT AUTO_INCREMENT,
            PRIMARY KEY (id),
            name VARCHAR(70) NOT NULL,
            url VARCHAR(500)
        )""")
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS 
        department_items (
            id INT AUTO_INCREMENT,
            PRIMARY KEY (id),
            name VARCHAR(100) NOT NULL,
            faculty VARCHAR(70) NOT NULL,
            url VARCHAR(500)
        )""")
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS 
        staff_items (
            id INT AUTO_INCREMENT,
            PRIMARY KEY (id),
            head_of_department VARCHAR(70) NOT NULL,
            address VARCHAR(70) NOT NULL,
            phone VARCHAR(20) NOT NULL,
            email VARCHAR(40) NOT NULL,
            department VARCHAR(100) NOT NULL
        )""")
        spider.logger.info("DB is ready ")

    def close_spider(self, spider):
        self.connection.close()
        spider.logger.info("Disconnected from MySQL ")

    def process_item(self, item, spider):
        if isinstance(item, FacultyItem):
            self.cursor.execute(
                "INSERT INTO faculty_items (name, url) VALUES (%s, %s);",
                [item.get("name"), item.get("url")])
        if isinstance(item, DepartmentItem):
            self.cursor.execute(
                "INSERT INTO department_items (name, faculty, url) VALUES (%s, %s, %s);",
                [item.get("name"), item.get('faculty'), item.get("url")])
        if isinstance(item, StaffItem):
            self.cursor.execute(
                "INSERT INTO staff_items (head_of_department, address, phone, email, department) VALUES (%s, %s, %s, %s, %s);",
                [item.get("head_of_department"), item.get('address'), item.get("phone"), item.get('email'), item.get("department")])
        self.connection.commit()
        return item
