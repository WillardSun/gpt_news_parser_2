import requests
import numpy as np

from auth import news_api_token, requesturl
from bs4 import BeautifulSoup
from gpt import askgpt
from user import User
from util import returnTopbySource, parseUrl

serverres = requests.get(requesturl)
serverres.raise_for_status()
response = serverres.json()
runs = 0

user = User()
user.changesortMode(input("Your desired sort mode? (0) Top headlines in HK | (1) By source :   "))
if user.sortMode == "by source": user.changeSource(input("Your desired source? (0) 雅虎 | (1) 香港01 | (2) 星島頭條 :   "))

match user.sortMode:
    case "top HK":
        print(f'Total responses: {response["totalResults"]}')
        for article in response['articles']:
            paragraphs = parseUrl(article['url'], article['author'])
            if (paragraphs == "next"): continue
            print(paragraphs)
            cont = int(input ("Use ChatGPT? (0) No | (1) Yes:   "))
            if cont == 1:
                print("\n\n\n===============================================+ CHAT GPT +===========================================")
                user.changeresMode(input("Your desired response type? (0) Summarise | (1) Positive | (2) Negative :   "))
                print(askgpt(paragraphs, user))
                input("Enter to continue")
            print(chr(27) + "[2J")
                
    case "by source":
        urls = returnTopbySource(user.source, user)
        for url in urls:
            paragraphs = parseUrl(url, user.source)
            print(paragraphs)
            cont = int(input ("Use ChatGPT? (0) No | (1) Yes:   "))
            if cont == 1:
                print("\n\n\n===============================================+ CHAT GPT +===========================================")
                user.changeresMode(input("Your desired response type? (0) Summarise | (1) Positive | (2) Negative :   "))
                print(askgpt(paragraphs, user))
                input("Enter to continue")
            print(chr(27) + "[2J")