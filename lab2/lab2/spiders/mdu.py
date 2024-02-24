import scrapy
from bs4 import BeautifulSoup
from lab2.items import FacultyItem, DepartmentItem, StaffItem

class MduSpider(scrapy.Spider):
    name = "mdu"
    allowed_domains = ["msu.edu.ua"]
    start_urls = ["https://msu.edu.ua/fakulteti"]

    def parse(self, response):
        faculty_soup = BeautifulSoup(response.body, 'html.parser')
        faculties_ul  = faculty_soup.find("article").find_all('ul')
        for faculty_ul in faculties_ul:
            faculty_item = faculty_ul.find_previous_sibling()
            faculty_name = faculty_item.findChildren("strong")[0].find(string=True)
            faculty_href = faculty_item.findChildren("a")[0].get('href')

            yield FacultyItem(
                name = faculty_name,
                url = faculty_href
            )
            departments_a = faculty_ul.findChildren("a")
            for department_a in departments_a:
                department_name = department_a.find(string = True)
                department_href = department_a.get('href')
                yield DepartmentItem(
                    name = department_name,
                    url = department_href,
                    faculty = faculty_name
                )
                yield scrapy.Request(
                    url=department_href,
                    callback=self.parse_department,
                    meta={
                        "department" : department_name
                    }
                )

    def parse_department(self, response):
        department_soup = BeautifulSoup(response.body, 'html.parser')
        td_with_name = department_soup.find("td", string="Назва")
        if td_with_name:
            department_info_table = td_with_name.find_parent("table")
            department_info_table_tds = department_info_table.findChildren("td")
            yield StaffItem(
                head_of_department = department_info_table_tds[3].find(string=True),
                address = department_info_table_tds[5].find(string=True),
                phone = department_info_table_tds[7].find(string=True),
                email = department_info_table_tds[9].find(string=True),
                department = response.meta.get('department')
            )