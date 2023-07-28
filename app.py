import requests
import numpy as np
import PySimpleGUI as sg

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


def askGPTwindow():
    layout4 = [[sg.Button('Start', key = 'start')],
               [sg.Text(size=(100, 20), font = ('Calibri', 15), key = 'news article')],
               [sg.Text("Use ChatGPT?", key = 'gpt prompt', visible = False)],
               [sg.Button('Yes', key = 'parse', visible = False), sg.Button('No', key = 'no parse', visible = False)],
               [sg.Text("Your desired response type? (0) Summarise | (1) Positive | (2) Negative :", key = 'res prompt', visible = False), sg.Input(size=(40, 1), key = 'response type', visible = False)],
               [sg.Button('Ask!', key = 'ask', visible = False)],
               [sg.Text(size=(100, 20), font = ('Calibri', 15), key = 'chatgpt out')],
               [sg.Button('Continue', key = 'continue', visible = False)]]
    window4 = sg.Window('Ask GPT', layout4)
    event, values = window4.read()
    window4['start'].Update(visible=False)
    urls = []
    if (user.sortMode == 1):
        for article in response['articles']:
            urls.append(article['url'])
    else: 
        urls = returnTopbySource(user.source, user)

    next = 0
    for url in urls:
        if (next): next = 0 
        paragraphs = parseUrl(url, user.source)
        window4['news article'].update(paragraphs)
        window4['gpt prompt'].Update(visible = True)
        window4['parse'].Update(visible = True)
        window4['no parse'].Update(visible = True)
        event, values = window4.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        if event == "parse":
            window4['res prompt'].Update(visible = True)
            window4['response type'].Update(visible = True)
            window4['ask'].Update(visible = True)
            while True:
                if (next == 1): break
                event, values = window4.read()
                if (event == "ask"):
                    user.changeresMode(int(values['response type']))
                    response = askgpt(paragraphs, user)
                    window4['chatgpt out'].Update(response)
                    window4['continue'].Update(visible = True)
                    while True:
                        event, values = window4.read()
                        if event == 'continue':
                            next = 1
                            window4['chatgpt out']. Update('')
                            window4['res prompt'].Update(visible = False)
                            window4['response type'].Update(visible = False)
                            window4['ask'].Update(visible = False)
                            window4['continue'].Update(visible = False)
                            break
        elif event == "no parse":
            continue

def chooseSourceWindow():
    window.close()
    layout3 = [[sg.Text('Your desired source? (0) 雅虎 | (1) 香港01 | (2) 星島頭條 :'), sg.InputText(key='source')],
          [sg.Button('Ok'), sg.Button('Cancel')]
          ]
    window3 = sg.Window('Choose your source', layout3)
    while True:
        event, values = window3.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        if values['source'] == '0' or values['source'] == '1' or values['source'] == '2':
            user.changeSource(int(values['source']))
            window3.close()
            askGPTwindow()


sg.theme('DarkAmber')
layout = [[sg.Text('Your desired sort mode? (0) Top headlines in HK | (1) By source :'), sg.InputText(key='sort mode')],
          [sg.Button('Ok'), sg.Button('Cancel')]
          ]
window = sg.Window('gpt news parser', layout)

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
        break
    if values['sort mode'] == '1':
        user.changesortMode(1)
        window.close()
        chooseSourceWindow()
        break
    elif values ['sort mode'] == '0':
        user.changesortMode(1)
        window.close()
        askGPTwindow()

window.close()