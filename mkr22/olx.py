import requests
from bs4 import BeautifulSoup
import csv


def extract_data_from_page(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    items = []

    ads = soup.find_all('a', class_='css-z3gu2d')[:50]  # дістає посилання на оголошення
    for ad in ads:
        try:
            ad_url = 'https://www.olx.ua/' + ad['href']
            print(ad_url)
            ad_response = requests.get(ad_url)
            ad_soup = BeautifulSoup(ad_response.text, 'html.parser')

            title = ad_soup.find('h4', class_='css-1juynto').text.strip()  # дістає назву
            price = ad_soup.find('h3', class_='css-12vqlj3').text.strip()  # дістає ціну
            location_data = ad_soup.find_all('p', class_='css-1cju8pu')
            if len(location_data) == 0:
                location = ""
            else:
                location = ad_soup.find_all('p', class_='css-1cju8pu')[0].text.strip()  # дістає місто
            date = ad_soup.find('span', class_='css-19yf5ek').text.strip()  # дістає дату

            items.append({
                'title': title,
                'price': price,
                'date': date,
                'location': location
            })
        except:
            print('error')

    return items


def save_to_csv(data, filename):
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['title', 'price', 'date', 'location']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for item in data:
            writer.writerow(item)


data = []
for i in range(2):
    if i == 0:
        continue
    print(f'Parsing this page {i} from 10')
    url = f'https://www.olx.ua/uk/list/q-принтер/?page={i}'
    data += extract_data_from_page(url)
save_to_csv(data, 'printers.csv')
