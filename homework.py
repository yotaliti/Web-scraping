import requests
import bs4
from fake_headers import Headers
from pprint import pprint


def get_fake_headers():
    return Headers(browser='chrome', os='win').generate()


KEYWORDS = ['дизайн', 'фото', 'web', 'python']

response = requests.get("https://habr.com/ru/articles/", headers=get_fake_headers())
soup = bs4.BeautifulSoup(response.text, features='lxml')

news_list = soup.findAll('article', class_="tm-articles-list__item")

parsed_data = []
for news in news_list:
    article_link = news.find('a', class_="tm-title__link")['href']
    response = requests.get(f'https://habr.com{article_link}', headers=get_fake_headers())
    article = bs4.BeautifulSoup(response.text, features='lxml')
    text = article.find('article', class_="tm-article-presenter__content tm-article-presenter__content_narrow").text
    for word in KEYWORDS:
        if f' {word} ' in text:
            title = article.find('h1').text
            time = article.find('time')['datetime']
            article_info = f'<{time[:10]} {time[11:19]}> – <{title}> – <https://habr.com{article_link}>'
            if article_info not in parsed_data:
                parsed_data.append(article_info)
pprint(parsed_data)
