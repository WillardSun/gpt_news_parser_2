from bs4 import BeautifulSoup
import requests
import numpy as np
from user import User

def returnTopbySource(source, user):
    url = user.sources[source]
    urls = []

    soup = BeautifulSoup(requests.get(url).content, "html.parser")
    match user.source: 
        case "星島頭條": body = soup.find_all(class_='news-detail')
        case "香港01": body = soup.find_all('span', class_ = 'Box-v1-cltunW kGMtBp sc-1nfazpo-0 fCwjCB jvqc0e-6 iqoqdg')
        case "雅虎香港新聞": body = soup.find_all('a', class_='D(ib) Ov(h) Whs(nw) C($c-fuji-grey-l) C($c-fuji-blue-1-c):h Td(n) Fz(16px) Tov(e) Fw(700) Lh(20px)')
    
    if user.source == "香港01" or user.source == "星島頭條":
        for span in body:
            tag = span.find_all('a', href=True)
            if (tag != []): 
                str = user.sources[user.source] + tag[0]['href']
                str.replace("'", "")
                str += 'html'
                urls.append(str)

    else:
        for i in body:
            urls.append(i['href'])

    return (urls)

def parseUrl (url, source):
    #print(url)
    article2 = requests.get(url)
    article_content = article2.content
    soup_article = BeautifulSoup(article_content, 'html.parser')
    body = []
    match source:
        case "星島頭條": body = soup_article.find_all('div', class_='content-body')
        case "香港01": body = soup_article.find_all('div', class_='article-grid__content-section')
        case "雅虎香港新聞": body = soup_article.find_all('div', class_='caas-body')
        case _: return "next"
    
    x = body[0].find_all('p')
            
    paragraphs = ""
    for p in np.arange(0,len(x)):
        paragraph = x[p].get_text()
        paragraphs += (paragraph + '\n')

    return paragraphs
