import random, sqlite3
import pandas as pd

def getDBConnection():
    conn = sqlite3.connect('smartkits.db')
    conn.row_factory = sqlite3.Row
    return conn

def storeResults(dfResponses):
    conn = getDBConnection()
    dfResponses.to_sql('quiz_responses', conn, if_exists='append', index=False)
    conn.close()

class Quiz():
    def __init__(self, name, listItems, sampleSize):
        def findId(name):
            query = '''
                SELECT
                    `quizzes`.`id` AS `id`
                FROM `quizzes`
                WHERE `quizzes`.`name` = "''' + str(name) + '"'

            conn = getDBConnection()

            try:
                id = conn.execute(query).fetchone()[0]
            except:
                id = None
            else:
                id = id
            finally:
                return id

        self.name = name
        self.listItems = listItems
        self.sampleSize = sampleSize
        self.id = findId(self.name)

    def getName(self):
        return self.name
    
    def getListItems(self):
        return self.listItems
    
    def getSampleSize(self):
        return self.sampleSize
    
    def getId(self):
        return self.id
    
    def getRandomItems(self):
        if(self.sampleSize == 0):
            return "Sample size should be greater than 0"
        elif(self.sampleSize > len(self.listItems)):
            return "Sample size should be lower than total number of items"
        else:
            randomItems = random.sample(self.listItems, self.sampleSize)
            dfQuestions = pd.DataFrame({"questions": randomItems})
            self.dfQuestions = dfQuestions
    
    def getDfQuestions(self):
        return self.dfQuestions
