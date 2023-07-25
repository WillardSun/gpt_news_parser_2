from bs4 import BeautifulSoup
import requests
import numpy as np

url = "https://www.stheadline.com/hit/%E6%9C%80Hit"
urls = []

soup = BeautifulSoup(requests.get(url).content, "html.parser")
for span in soup.find_all(class_='news-detail'):
    tag = span.find_all('a', href=True)
    if (tag != []):
        str = "https:\\stheadline.com" + tag[0]['href']
        str.replace("'","")
        str += '.html'
        urls.append(str)

print(urls)
