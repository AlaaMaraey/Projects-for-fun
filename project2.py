
from requests_html import HTMLSession
from urllib.parse import urljoin

def get_synopsis(url):
    s2 = HTMLSession()
    r2 = s2.get(url)
    r2.html.render()
    divs = r2.html.find("div[class='anime-synopsis']" )
    p = divs[0].text
    anchor = r2.html.find('a', containing='myanimelist')
    Link = anchor[0].attrs['href']
    return p, Link

def get_myanime_list(url):
    url = 'http:' + url
    s3 = HTMLSession()
    r3 = s3.get(url)
    divs = r3.html.find("div[class='score-label score-6']")
    score = divs[0].text
    return score


try: 
        
    s = HTMLSession()
    base_url = "https://animepahe.com/"

    r = s.get(base_url)

    r.html.render(sleep=2)
    
    spans = r.html.find('span a')
    names= []
    links = []
    full_links = []
    syn = []
    scores = []
    for item in spans:
        names.append(item.attrs['title']),
        links.append(item.attrs['href'])

    for link in links:
        full_links.append(urljoin(base_url, link))

    
    for link in full_links[0:2]:
        [syno, anime_list] = get_synopsis(link)
        score = get_myanime_list(anime_list)
        syn.append(syno)
        scores.append(score)
        

    anime_dict = {
        'name' : names,
        'links' : full_links,
        'synopsis' : syn,
        'scores'  : scores
    }
    

    print(anime_dict['scores'])    
    r.close()
    s.close()

except OSError:
    pass
except ConnectionResetError:
    pass