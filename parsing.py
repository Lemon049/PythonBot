import requests
from bs4 import BeautifulSoup
import pandas as pd

url = 'https://funpay.com/en/lots/1408/'

response = requests.get(url)
html_doc = response.text

soup = BeautifulSoup(html_doc, 'html.parser')

items = soup.find_all('a', class_='tc-item')

data = []

for item in items:
    link = item.get('href', '')
    platform = item.get('data-f-platform', '')
    edition = item.get('data-f-type', '')
    region = item.get('data-f-region', '')
    activation_type = item.get('data-f-method', '')
    price_div = item.find('div', class_='tc-price')
    price = price_div.get_text(strip=True).replace('€', '').strip() if price_div else ''
    seller_div = item.find('div', class_='media-user-name')
    seller = seller_div.get_text(strip=True) if seller_div else ''
    rating_span = item.find('span', class_='rating-mini-count')
    rating = rating_span.get_text(strip=True) if rating_span else ''
    stars_div = item.find('div', class_='rating-stars')
    stars = stars_div['class'][1].split('-')[-1] if stars_div and 'class' in stars_div.attrs else ''
    avatar_photo_div = item.find('div', class_='avatar-photo')
    seller_profile = avatar_photo_div['data-href'] if avatar_photo_div and 'data-href' in avatar_photo_div.attrs else ''

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