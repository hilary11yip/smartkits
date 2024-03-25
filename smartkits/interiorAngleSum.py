from quiz import Quiz
import random, re

class interiorAngleSumQuizGenerator(Quiz):
    def __init__(self, name, sampleSize):
        def createListOfAngles(side, isPolygon):
            angles = list(range(0, side))
            angleSum = 180 * (side - 2)
            remaining = angleSum
            for i in range(side):
                lastSide = (i == (side - 1) )
                if(lastSide):
                    if(isPolygon):
                        angles[i] = remaining
                else:
                    angles[i] = random.randint(1, remaining)
                    remaining -= angles[i]
            return angles
        
        def createListOfQuestions(sampleSize):
            listItems = []
            for i in range(sampleSize + 1):
                side = 3
                isPolygon = bool(random.randint(0, 1))
                listItems.append(createListOfAngles(side, isPolygon))
            return listItems

        listItems = createListOfQuestions(sampleSize)
        Quiz.__init__(self, name, listItems, sampleSize)

    def getCorrectAns(self):
        pattern = r'\d+'
        sumRow = lambda x: sum(int(num) for num in re.findall(pattern, str(x)))
        self.dfQuestions['angleSum'] = self.dfQuestions['questions'].apply(sumRow)
        self.dfQuestions['numberOfSides'] = self.dfQuestions['questions'].apply(lambda x: len(x))
        self.dfQuestions['correctAngleSum'] = (self.dfQuestions['numberOfSides'] - 2) * 180