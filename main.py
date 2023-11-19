import requests
from bs4 import BeautifulSoup
import json

def parser(base_url):
    quotes = list()
    authors = list()
    count = 0

    while True:
        count += 1
        url = f'{base_url}/page/{count}'
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'lxml')
        
        div_quote = soup.find_all('div', class_='quote')
        if not div_quote:
            break
        for el in div_quote:
            quote = el.find('span', class_='text').text
            author = el.find('small', class_='author').text
            author_links = soup.find('a', href=lambda href: href and 'author' in href)['href']
            all_tags = el.find_all('div', class_='tags')

            for _ in all_tags:
                tag_links = _.find_all('a')
                tags = list()
                for tag_link in tag_links:
                    tags.append(tag_link.text)
            new_request = BeautifulSoup(requests.get(f'{base_url}/{author_links}').text, 'lxml')
            quotes.append({
                "tags": tags,
                "author": author,
                "quote": quote
            })
            authors.append({
                "fullname": author,
                "born_date": new_request.find('span', class_='author-born-date').text,
                "born_location": new_request.find('span', class_='author-born-location').text,
                "description": quote
            })
        
    with open('quotes.json', 'w', encoding='utf-8') as fl:
        json.dump(quotes, fl, indent=2)
    with open('authors.json', 'w', encoding='utf-8') as fl:
        json.dump(authors, fl, indent=2)

url = 'https://quotes.toscrape.com'

parser(url)
