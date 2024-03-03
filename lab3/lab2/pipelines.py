# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from re import search
from scrapy.exceptions import DropItem
from lab2.items import StaffItem, DepartmentItem, FacultyItem

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