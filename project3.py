'''
Scraping the front page of hackernews using requests_HTML
The code scrapes the fron page only and stores the data in dict

'''
from requests_html import HTMLSession
import re

base_url = "https://news.ycombinator.com/news"
session = HTMLSession()
request = session.get(base_url)

links = []
titles = []
scores = []
comments_count = []

#Extracting the title & the link to the page 
table_row = request.html.find("tr.athing")
for item in table_row:
    a_item = item.find('a.storylink')
    link = a_item[0].attrs['href']
    title = a_item[0].text
    titles.append(title)
    links.append(link)
    
#Getting the score
exp1 = re.compile('[points]')
points = [score.text for score in request.html.find('span.score')]
for point in points:
    point = re.sub(exp1,'', point)
    scores.append(float(point.strip()))

#Getting the count of the comments
cell_items = request.html.find('td.subtext')
exp2 = re.compile(r'[/d+\xa0comments]') #getting only the number

for anchor in cell_items:
    comments = anchor.find('a', containing = "\xa0comments")
    if len(comments) == 0:
        comment_count = '0'
    else:
        for comment in comments:
            comment_count = re.sub(exp2, '', comment.text)
    comments_count.append(float(comment_count.strip()))
    #converting them inot numerical values
                       

print(len(comments_count), len(scores))
data = {
    'Titles' : titles,
    'Links' : links,
    'Scores' : scores,
    'Comments Count' : comments_count
        }
session.close()