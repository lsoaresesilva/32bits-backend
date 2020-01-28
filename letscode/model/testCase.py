from letscode.model.errors.testCaseError import TestCaseError
# a fazer, testar execução. adaptar para testes case na classe
class TestCase():

    def __init__(self, id, entradas, saida):
        if not entradas or (type(entradas) != list and len(entradas) == 0): 
            raise ValueError("Entradas inválidas para TestCase")
        
        if saida == None:
            raise ValueError("Saída inválida para TestCase")

        self.id = id
        self.entradas = entradas
        self.saida = saida
        

    def isValido(self):
        if not self.entradas or len(self.entradas) == 0 or self.saida == "" or not self.saida:
            return False

        return True

    @staticmethod
    def isTestsValidos(testCases):
        if testCases == None or not testCases:
            return False

        try:
            iter(testCases)
            return True
        except TypeError as te:
            return False

    @staticmethod
    def validarJson(jsonData):
        if jsonData["id"] != None and jsonData["entradas"] != None and jsonData["saida"] != None:
            return True
        return False

    @staticmethod
    def fromJson(jsonData):
        if TestCase.validarJson(jsonData):
            return TestCase(jsonData["id"], jsonData["entradas"], jsonData["saida"])

        