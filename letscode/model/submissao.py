from letscode.model.questao import Questao

class Submissao():

    def __init__(self, codigo, questao):
        self.codigo = codigo
        self.questao = questao
        self.resultadosTestsCases = []
        self.saida = None

    def getSaida(self):
        saidaAlgoritmo = []
        if self.saida != None and len(self.saida) > 0:
            for resultado in self.saida.split("\r\n"):
                if resultado != "" and resultado != "\r" and resultado != "\n":
                    saidaAlgoritmo.append(resultado)
        return saidaAlgoritmo

    def toJson(self):
        
        resultados = []
        for resultado in self.resultadosTestsCases:
            resultados.append(resultado.toJson())

        #saidaAlgoritmo = self.getSaida()
        
        return {
            "resultados":resultados,
            #"saida":self.saida
        }
    
    @staticmethod
    def fromJson(jsonData):
        return Submissao(jsonData["submissao"]["codigo"], Questao.fromJson(jsonData["questao"]))

    @staticmethod
    def validarJson(jsonData):
        if jsonData["tipo"] != None and jsonData["submissao"] != None and jsonData["submissao"] != "" and jsonData["submissao"]["codigo"] != "" and jsonData["questao"] != None and jsonData["questao"] != "":
            return True

        return False

        