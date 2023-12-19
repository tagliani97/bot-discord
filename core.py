import re
import requests
from bs4 import BeautifulSoup

def extract_data(text):
    pattern = r'\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) \d{1,2}, \d{4} \d{1,2}:\d{2} [APM]{2}\b'
    match = re.search(pattern, text)
    return match.group(0) if match else ""

def print_item(item_name, item_type, item_date, attachments):
    print(f"item: {item_name}")
    print(f"tipo: {item_type}")
    print(f"data: {extract_data(item_date)}")
    print("loudout:")
    for attachment in attachments:
        attachment_type = attachment.find('span').get_text(strip=True)
        attachment_name = attachment.find('div', class_='attachment-card-content__name').div.get_text(strip=True)
        print(f"    - {attachment_type}: {attachment_name}")
    print('---------------')

def get_response(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        loadouts_group = soup.find('div', class_='loadouts-list__group')
        item_box = loadouts_group.find_all('div', class_='wrap-card__content')

        for item in item_box:
            item_name = item.find('div', class_='gun-badge__text').get_text(strip=True)
            item_type = item.find('div', class_='expand-card__el loadout-card__type').get_text(strip=True).replace("Warzone", "").strip()
            item_date = item.find('div', class_='expand-card__author').get_text(strip=True).strip()
            attachments = item.find_all('div', class_='attachment-card')

            print_item(item_name, item_type, item_date, attachments)

    except requests.RequestException as e:
        print(f"Error fetching data from {url}: {e}")


url = 'https://wzhub.gg/loadouts'
get_response(url)
