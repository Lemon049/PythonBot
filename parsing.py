import requests
from bs4 import BeautifulSoup
import pandas as pd

import main


def find_game_key_link(funpay_url, game_title):
    response = requests.get(funpay_url)
    if response.status_code != 200:
        print("Failed to retrieve the webpage")
        return None

    soup = BeautifulSoup(response.content, 'html.parser')

    game_items = soup.find_all('div', class_='promo-game-item')

    for game_item in game_items:
        title_div = game_item.find('div', class_='game-title')
        if title_div and title_div.get_text(strip=True) == game_title:
            ul_list = game_item.find('ul', {'data-id': title_div['data-id']})
            if ul_list:
                for li in ul_list.find_all('li'):
                    if li.get_text(strip=True) == 'Keys':
                        link = li.find('a', href=True)['href']
                        return link

    return None


# Translation dictionary
edition_translation_dict = {
    "улучшение издания": "Edition upgrade"
}

region_translation_dict = {
    "россия": "Russia",
    "украина": "Ukraine",
    "казахстан": "Kazakhstan",
    "снг": "CIS",
    "другой регион": "Other region",
    "турция": "Turkey",
    "аргентина": "Argentina"
}

activation_type_translation_dict = {
    "с заходом на аккаунт": "By logging into the account",
    "цифровой ключ": "Digital Key",
    "подарком": "Gift"
}


def replace_text_using_dict(text, translation_dict):
    if text in translation_dict:
        return translation_dict[text]
    return text


def funpay_parsing(game_title):
    funpay_url = 'https://funpay.com/en/'
    link = find_game_key_link(funpay_url, game_title)
    response = requests.get(link)
    html_doc = response.text

    soup = BeautifulSoup(html_doc, 'html.parser')

    items = soup.find_all('a', class_='tc-item')

    data = []

    t = items[1].get('data-f-type', '')

    for index, item in enumerate(items):
        print(f"Processing item {index + 1}/{len(items)}")

        link = item.get('href', '')

        platform = item.get('data-f-platform', '')
        if not platform:
            platform_div = item.find('div', class_='tc-server-inside')
            platform = platform_div.get_text(strip=True) if platform_div else ''

        edition = item.get('data-f-type', '')
        region = item.get('data-f-region', '')
        activation_type = item.get('data-f-method', '')

        edition = replace_text_using_dict(edition, edition_translation_dict)
        region = replace_text_using_dict(region, region_translation_dict)
        activation_type = replace_text_using_dict(activation_type, activation_type_translation_dict)

        price_div = item.find('div', class_='tc-price')
        price = price_div.get_text(strip=True).replace('€', '').strip() if price_div else ''

        seller_div = item.find('div', class_='media-user-name')
        seller = seller_div.get_text(strip=True) if seller_div else ''

        rating_span = item.find('span', class_='rating-mini-count')
        rating = rating_span.get_text(strip=True) if rating_span else ''

        stars_div = item.find('div', class_='rating-stars')
        stars = stars_div['class'][1].split('-')[-1] if stars_div and 'class' in stars_div.attrs else ''

        avatar_photo_div = item.find('div', class_='avatar-photo')
        seller_profile = avatar_photo_div[
            'data-href'] if avatar_photo_div and 'data-href' in avatar_photo_div.attrs else ''

        data.append({
            'Link': link,
            'Platform': platform,
            'Edition': edition,
            'Region': region,
            'Activation type': activation_type,
            'Price': price,
            'Seller': seller,
            'Rating': rating,
            'Stars': stars,
            'Seller Profile': seller_profile
        })

    df = pd.DataFrame(data)

    df.to_excel('scraped_data.xlsx', index=False)

    print("Data scraping completed.")



