# 1. Знайти відкрите джерело даних, що містить список підрозділів з URL для переходу на сторінку цього підрозділу. Кожна із сторінок повинна  містити список деяких об'єктів. 
# Наприклад, це може бути сайт університету, що містить список факультетів, кафедр та викладачів.
# URL обраного джерела вказати в коментарі.

# Мукачівський державний університет, факультети: https://msu.edu.ua/fakulteti/

#2. Переконатись, що сторінки є статичними. Використовуючи бібліотеку requests завантажити сторінку зі списком та вивести в консоль.
from requests import get

url = "https://msu.edu.ua/fakulteti/"
response_page = get(url)

print(response_page.text)
print(f"Status code: {response_page.status_code}")
print("========================================")

# 3. Використовуючи бібліотеку Beautiful soap отримати список підрозділів та їх URL .
from bs4 import BeautifulSoup

faculty_soup = BeautifulSoup(response_page.content, 'html.parser')
faculties_ul  = faculty_soup.find("article").find_all('ul')

for faculty_ul in faculties_ul:
    faculty_name = faculty_ul.find_previous_sibling().findChildren("strong")[0].find(string=True)
    print(faculty_name)
    departments_a = faculty_ul.findChildren("a")
    for department_a in departments_a:
        department_name = department_a.find(string = True)
        department_href = department_a.get('href')
        print(f"{department_name}: {department_href}")

print("===========================================")

#4. Використовуючи запити отримати списки із кожної зі сторінок підрозділів.
for faculty_ul in faculties_ul:
    departments_a = faculty_ul.findChildren("a")
    faculty_name = faculty_ul.find_previous_sibling().findChildren("strong")[0].find(string=True)
    print(faculty_name)

    for department_a in departments_a:
        department_name = department_a.find(string = True) 
        department_href = department_a.get('href')

        response_department_page = get(department_href)
        department_soup = BeautifulSoup(response_department_page.content, 'html.parser')

        td_with_name = department_soup.find("td", string="Назва")
        if td_with_name:
            department_info_table = td_with_name.find_parent("table")
        department_info_table_td = department_info_table.findChildren("td")
        for i in range(int(len(department_info_table_td)/2)-1):
            print(f"{department_info_table_td[i*2].find(string=True)}: {department_info_table_td[i*2+1].find(string=True)}")

print("============================================")

# 5. Зберегти результати скрапінгу до текстового файлу.
FILE_NAME = "Lab1/mdu.txt"
with open(FILE_NAME, "w", encoding="utf-8") as file:
    for faculty_ul in faculties_ul:
        departments_a = faculty_ul.findChildren("a")
        faculty_name = faculty_ul.find_previous_sibling().findChildren("strong")[0].find(string=True)
        file.write(f"\nНазва факультету: {faculty_name}\n")

        for department_a in departments_a:
            department_name = department_a.find(string = True) 
            department_href = department_a.get('href')
            file.write(f"\n   Назва кафедри: {department_name}\n")
            file.write(f"   URL: {department_href}\n")
            response_department_page = get(department_href)
            department_soup = BeautifulSoup(response_department_page.content, 'html.parser')

            td_with_name = department_soup.find("td", string="Назва")
            if td_with_name:
                department_info_table = td_with_name.find_parent("table")
            department_info_table_td = department_info_table.findChildren("td")
            file.write(f"   Інформація про кафедру:\n")
            for i in range(int(len(department_info_table_td)/2)-1):
                file.write(f"        {department_info_table_td[i*2].find(string=True)} - {department_info_table_td[i*2+1].find(string=True)}\n")