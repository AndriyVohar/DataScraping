import scrapy

from lab2.items import FacultyItem, DepartmentItem, StaffItem

class MduSpider(scrapy.Spider):
    name = "mdu"
    allowed_domains = ["msu.edu.ua"]
    start_urls = ["https://msu.edu.ua/fakulteti"]

    def parse(self, response):
        faculties = response.css('article p a')
        list_of_counters = [0]
        list_of_faculties = []
        for faculty in faculties:
            faculty_strong = faculty.css('strong')
            if(faculty_strong):
                faculty_name = faculty.css('strong::text').get()
                faculty_href = faculty.css('a::attr(href)').get()
                yield FacultyItem(
                    name=faculty_name,
                    url=faculty_href
                )
                list_of_counters+=[list_of_counters[-1]+1]
                list_of_faculties+=[faculty.css('strong::text').get()]
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
            ul = response.css('article ul')
            for department in ul[count].css('li a'):
                department_name = department.css('::text').get()
                department_href = department.css('::attr(href)').get()
                yield DepartmentItem(
                    name=department_name,
                    url=department_href,
                    faculty=faculties[count]
                )
                yield scrapy.Request(
                    url=department_href,
                    callback=self.parse_department,
                    meta={
                        'department': department_name
                    }
                    
                )
    def parse_department(self, response):
        department_info_table = response.css('table:contains("Назва")')
        department_info_table_tds = department_info_table.css('td')

        yield StaffItem(
            head_of_department=department_info_table_tds[3].css('::text').get(),
            address=department_info_table_tds[5].css('::text').get(),
            phone=department_info_table_tds[7].css('::text').get(),
            email=department_info_table_tds[9].css('::text').get(),
            department=response.meta.get('department')
        )
