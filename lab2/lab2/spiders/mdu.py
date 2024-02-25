import scrapy

from lab2.items import FacultyItem, DepartmentItem, StaffItem

class MduSpider(scrapy.Spider):
    name = "mdu"
    allowed_domains = ["msu.edu.ua"]
    start_urls = ["https://msu.edu.ua/fakulteti"]

    def parse(self, response):
        faculties = response.xpath('//article//a[strong]')
        list_of_counters = [1]
        list_of_faculties = []
        for faculty in faculties:
            faculty_name = faculty.xpath('./strong/text()').get()
            faculty_href = faculty.xpath('@href').get()
            yield FacultyItem(
                name=faculty_name,
                url=faculty_href
            )
            list_of_counters+=[list_of_counters[-1]+1]
            list_of_faculties+=[faculty_name]
        list_of_counters = list_of_counters[:-1]
        yield scrapy.Request(
            url="https://msu.edu.ua/fakulteti",
            callback=self.parse_faculty,
            meta={"faculty": list_of_faculties, "counter": list_of_counters}
        )
    def parse_faculty(self, response):
        counter = response.meta.get('counter')
        faculties = response.meta.get('faculty')
        for count in counter:
            ul = response.xpath(f'//article//ul[{count}]')
            for department in ul.xpath('./li/a'):
                department_name = department.xpath('./text()').get()
                department_href = department.xpath('@href').get()
                yield DepartmentItem(
                    name=department_name,
                    url=department_href,
                    faculty=faculties[count-1]
                )
                yield scrapy.Request(
                    url=department_href,
                    callback=self.parse_department,
                    meta={
                        'department': department_name
                    }
                )
    def parse_department(self, response):
        department_info_table = response.xpath('//table[contains(., "Назва")]')
        department_info_table_tds = department_info_table.xpath('.//td')

        yield StaffItem(
            head_of_department=department_info_table_tds[3].xpath('string()').get(),
            address=department_info_table_tds[5].xpath('string()').get(),
            phone=department_info_table_tds[7].xpath('string()').get(),
            email=department_info_table_tds[9].xpath('string()').get(),
            department=response.meta.get('department')
        )

