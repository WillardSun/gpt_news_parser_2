import numpy as np

class User():
    def __init__(self):
        self.resModes = ["summarise", "positive", "negative"]
        self.sortModes = ["top HK", "by source"]
        self.sources = {"雅虎香港新聞": "https://hk.news.yahoo.com/", 
                        "香港01": "https://www.hk01.com/",
                        "星島頭條": "https://www.stheadline.com" 
                        }
        
        self.resMode = self.resModes[0]
        self.sortMode = self.sortModes[0]
        self.source = list(self.sources.keys())[0]

    def changeresMode(self, index):
        self.resMode = self.resModes[int(index)]
    def changesortMode(self, index):
        self.sortMode = self.sortModes[int(index)]
    def changeSource(self, index):
        self.source = list(self.sources.keys())[int(index)]





# User can choose response mode (userMode: summarise, positive, negative)
# sort by what (userSort: by source)
#  