import hashlib

import requests
from bs4 import BeautifulSoup
import psycopg2
from config import host, user, password, db_name


connection = psycopg2.connect(
    host = host,
    user = user,
    password = password,
    database = db_name,
)
connection.autocommit = True
cursor = connection.cursor()

#cursor.execute("INSERT INTO news (news_title, news_href, news_tags, news_time, news_img) VALUES ('Заголовок', 'ссылка', 'тэги', 'время', 'картинка')")


headers = {
    "Accept": "*/*",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5845.888 YaBrowser/23.9.2.888 Yowser/2.5 Safari/537.36"
}

url = 'https://iz.ru/feed'

req = requests.get(url, headers=headers)
src = req.text

soup = BeautifulSoup(src, 'lxml')
all_titles = soup.find_all(class_="lenta_news__day__list__item__title")
all_news = []
for item in all_titles:
    item_title = item.text.strip()
    item_href = "https://iz.ru" + item.parent.get('href')
    all_news.append([item_title, item_href])

for i in range(len(all_news)):
    news_title = all_news[i][0]
    news_href = all_news[i][1]

    req = requests.get(news_href, headers=headers)
    src = req.text
    soup = BeautifulSoup(src, 'lxml')

    news_date = soup.find('time').text

    hashtags = "{"
    news_hashtags = soup.find_all("div", itemprop='about')
    for j in range(len(news_hashtags)):
        if j == len(news_hashtags) - 1:
            hashtags += f'"{news_hashtags[j].text}"'
        else:
            hashtags += f'"{news_hashtags[j].text}", '

    hashtags += "}"



    img_href = "https:" + soup.find(class_="owl-lazy")['data-src']
    img = requests.get(img_href)
    img_title = hashlib.sha256(news_title.encode()).hexdigest()
    with open(f"static/media/{img_title}.jpg", "wb") as img_option:
        img_option.write(img.content)

    cursor.execute(f"INSERT INTO news (news_title, news_href, news_tags, news_time, news_img) "
                    f"VALUES ('{news_title}', '{news_href}', '{hashtags}', '{news_date}', 'static/media/{img_title}.jpg')")



url = "https://ria.ru/lenta/"
req = requests.get(url, headers=headers)
src = req.text

soup = BeautifulSoup(src, 'lxml')
all_titles = soup.find_all(class_="list-item__title color-font-hover-only")
all_news = []
for item in all_titles:
    item_title = item.text
    item_href = item.get("href")
    all_news.append([item_title, item_href])

for i in range(len(all_news)):
    news_title = all_news[i][0].strip()
    news_href = all_news[i][1]

    req = requests.get(news_href, headers=headers)
    src = req.text
    soup = BeautifulSoup(src, 'lxml')

    news_date = soup.find(class_="article__info-date").text
    if "\n" in news_date:
        news_date = news_date[:news_date.find("\n")]
    all_news[i].append(news_date)

    hashtags = "{"
    news_hashtags = soup.find_all(class_="article__tags-item")
    for j in range(len(news_hashtags)):
        if j == len(news_hashtags) - 1:
            hashtags += f'"{news_hashtags[j].text}"'
        else:
            hashtags += f'"{news_hashtags[j].text}", '

    hashtags += "}"

    # for k in range(len(news_title)):
    #     if news_title[k] == '"' or news_title[k] == "'":
    #         print("Эгегей")
    #         news_title = news_title[:k] + '\\' + news_title[k:]
    #         print("Поменял")
    img_href = soup.find("div", class_="photoview__open").img['src']
    img = requests.get(img_href)
    img_title = hashlib.sha256(news_title.encode()).hexdigest()
    with open(f"static/media/{img_title}.jpg", "wb") as img_option:
        img_option.write(img.content)

    cursor.execute(f"INSERT INTO news (news_title, news_href, news_tags, news_time, news_img) "
                    f"VALUES ('{news_title}', '{news_href}', '{hashtags}', '{news_date}', 'static/media/{img_title}.jpg')")
