from quiz import Quiz
import pandas as pd

class multiplicationQuizGenerator(Quiz):
    def __init__(self, name, sampleSize):
        def createListOfQuestions():
            baseNumbers = list(range(1, 10))
            multipliers = list(range(1, 10))
            listItems = []

            for baseNumber in baseNumbers:
                for multiplier in multipliers:
                    question = "{} X {}".format(baseNumber, multiplier)
                    listItems.append(question)
            return listItems
        
        listItems = createListOfQuestions()
        Quiz.__init__(self, name, listItems, sampleSize)
    
    def getCorrectAns(self):
        pattern = r'\d+'
        self.dfQuestions['numbers'] = self.dfQuestions['questions'].str.findall(pattern)
        self.dfQuestions['correctAns'] = self.dfQuestions['numbers'].apply(lambda x: 1 if len(x) == 0 else pd.Series(x, dtype=int).prod())

    