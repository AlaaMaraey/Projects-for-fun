from requests_html import HTMLSession
import pandas as pd
from urllib.parse import urljoin
import re

def get_data(links, df):
    i = 0
    exp = re.compile('\d+') #to get the price&& \d+ returns whole digits (\d) splits the digit
    for link in links:
        s = HTMLSession()
        r = s.get(link)
        x1 = r.html.find('div > h1')#title
        x2 = r.html.find('div > p') #price
        x3 =r.html.find("div [class='instock availability']")
        x4 = r.html.find("[href*='category']") #getting category
        
        if ('available' in x3[0].text): 
            available = 'Yes'
        else:
            available = 'No'
        stock = re.findall(exp, x3[0].text)#find all returns a list
        category = x4[1].text     

        #storing data in a data frame
        df = df.append({
            'Title' : x1[0].text,
            'Category' : category,
            'Available' : available,
            'Price in Euros' : float(x2[0].text.strip('£')),
            'Stock' : float(stock[0])
        }, ignore_index=True)
        i = i + 1
        print("Scraped items: %f" %(i))
        s.close()
        
    return df
        
#creating the data Frame
Data = pd.DataFrame()
links = [] #all internal links throught the site
anchors = [] #all anchor elements through the site
page = 0
s = HTMLSession()
base_url = "http://books.toscrape.com/" #Site to be scraped
r = s.get(base_url)

while page <= 20:
    page = page + 1
    print('page %s' %(page))
    anchors.extend(r.html.find('h3 > a')) #finding all anchor elements
    next_page_element= r.html.find("li[class='next']")
    if len(next_page_element) != 0:
        next_page_anchor = next_page_element[0].find('a')
        next_page_link = next_page_anchor[0].attrs['href']
        if 'catalogue'  not in next_page_link: #rewriting the link into the correct format
            next_page_link = 'catalogue/' + next_page_link
        new_url = urljoin(base_url, next_page_link) #adding the missing word
        r = s.get(new_url)
    else:
        break

s.close()        

for link in anchors:
    link = link.attrs['href']
    if 'catalogue' not in link:
        link = 'catalogue/' + link 
    links.append(urljoin(base_url, link))



Data = get_data(links, Data)
Data.to_excel("Scraped Books.xlsx", index= False)