from quiz import Quiz
import pandas as pd
import re, requests
from jsonpath_ng import parse

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

URL_DICT = 'https://api.datamuse.com/words'
URL_CEFR = 'https://www.englishprofile.org/wordlists/evp'
CEFR_LEVELS = ['A1', 'A2', 'B1', 'B2', 'C1', 'C2']

class igPictureGenerator(Quiz):
    def __init__(self, name, listItems, sampleSize):
        Quiz.__init__(self, name, listItems, sampleSize)

class igTagAnalyzer():
    def __init__(self, tags, quizId):
        def getWordsFromTags(tags):
            tags = re.sub(r'\s', '', tags)
            tags = tags.split('#')[1:]
            return tags

        self.tags = getWordsFromTags(tags)
        dfTags = pd.DataFrame({"tag": self.tags,
                               "quiz_id": [quizId] * len(self.tags),
                               "partOfSpeech": [''] * len(self.tags),
                               "cefr": [''] * len(self.tags),
                               "relatedWords": [''] * len(self.tags),
                               "meaning": [''] * len(self.tags),
                               "code": [''] * len(self.tags)
                            })
        self.dfTags = dfTags

    def getDFTags(self):
        return self.dfTags
    
    def findEnglishWordProfile(self):
        def findFirstElement(elements):
            if elements:
                return elements[0]
            else:
                return None
        
        def getDriver():
            chrome_options = Options()
            chrome_options.add_argument("--headless")
            driver = webdriver.Chrome(options=chrome_options)
            return driver
            
        for i, row in self.dfTags.iterrows():
            try:
                driver = getDriver()
                driver.get(URL_CEFR)
                driver.implicitly_wait(100)
            except:
                row["meaning"] = ''
                row["partOfSpeech"] = ''
                row["cefr"] = ''
            else:
                text_box = driver.find_element(By.ID, 'filter_search')
                text_box.send_keys(str(row["tag"]))
                text_box.send_keys(Keys.ENTER)
                driver.implicitly_wait(100)
                details = driver.find_elements(By.LINK_TEXT, "Details")
                detail = findFirstElement(details)
                detail.click()
                driver.implicitly_wait(100)
                elementsToFind = ["span.pos", "span.definition"]
                texts = []
                for item in elementsToFind:
                    if isinstance(item, str):
                        elements = driver.find_elements(By.CSS_SELECTOR, item)
                        firstItem = findFirstElement(elements)   
                    else:
                        elements = []
                    texts.append(firstItem.text)
                for item in CEFR_LEVELS:
                    elements = driver.find_elements(By.XPATH, f"//span[text()='{item}']")
                    firstItem = findFirstElement(elements)
                    if firstItem != None:
                        texts.append(firstItem.text)
                        break
                driver.quit()
                row["partOfSpeech"] = texts[0]
                row["meaning"] = texts[1]
                row["cefr"] = texts[2]
        
    def findRelatedWords(self):
        for i, row in self.dfTags.iterrows():
            if(row["partOfSpeech"] == 'verb'):
                row["code"] = 'sym'
            elif(row["partOfSpeech"] == 'noun'):
                row["code"] = 'jjb'
            elif(row["partOfSpeech"] == 'adjective'):
                row["code"] = 'jja'

            method = "rel_" + row["code"]
            params = {
                method: row["tag"],
                "topics": '',
                "max": 5
            }
            response = requests.get(URL_DICT, params=params)
            data = response.json()
            if data:
                relatedWords = [d['word'] for d in data]
                row["relatedWords"] = relatedWords
            else:
                row['relatedWords'] = ""
        