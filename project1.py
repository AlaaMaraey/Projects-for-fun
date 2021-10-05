import pandas as pd
from bs4 import BeautifulSoup as bs
import time
import requests
from urllib.parse import urljoin as uj



base_url = 'http://quotes.toscrape.com/'

def get_soup(url):
    src = requests.get(url)
    html = src.content
    sp = bs(html, 'lxml')
    return sp

# with open('Test.html', 'wb') as file:
#     file.write(soup.prettify('utf-8'))

Quotes = []
Authors = []
Tags = []
soup = get_soup(base_url)
x = 0
t = time.time()

while True:
    div_sections = soup.find_all('div', {"class" : "quote"})
    quotes = [txt.find('span', {'class' : "text"}).string for txt in div_sections]
    author = [name.find('small').text for name in div_sections]
    tag_section = [tags.find_all('a', {'class' : 'tag'})for tags in div_sections]
    tags = [", ".join([txt.string for txt in tag]) for tag in tag_section]

    next_page = soup.find_all('li' , {'class' : 'next'})
    if len(next_page) != 0:
        pass
    else:
        break
    link_page = next_page[0].find('a').get('href')
    page = uj(base_url, link_page)
    soup = get_soup(page)
    print(page)
    Authors.extend(author)
    Quotes.extend(quotes)
    Tags.extend(tags)
    x = x + 1
    
t = time.time() - t

minds_info = pd.DataFrame()

minds_info['Author'] = Authors
minds_info['Quote'] = Quotes
minds_info['Tags'] = Tags
minds_info.to_excel("quotes.xlsx",index=False,header=True)
# # pd.set_option('display.max_colwidth', -1)
print(t)


