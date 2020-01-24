from letscode.model.testCase import TestCase

class Questao():

    def __init__(self, testsCases):
        self.testsCases = testsCases

    @staticmethod
    def fromJson(data):
        testsCases = []
        for t in data["testsCases"]:
            testsCases.append(TestCase.fromJson(t))
        return Questao(testsCases)