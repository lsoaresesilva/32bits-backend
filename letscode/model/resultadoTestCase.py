from letscode.model.firestore.document import Document
from letscode.model.firestore.document import Collection
from letscode.model.firestore.query import Query

@Collection("resultadoTestCase")
class ResultadoTestCase(Document):

    def __init__(self, id, testCase, respostaAlgoritmo, status):
        super().__init__(id)
        self.testCase = testCase
        self.status = status
        self.respostaAlgoritmo = respostaAlgoritmo

    def objectToDocument(self):
        document = super().objectToDocument()
        document["testCaseId"] = self.testCase["id"]
        document["respostaAlgoritmo"] = self.respostaAlgoritmo
        return document

    def __eq__(self, other):
        return self.testCase.id == other.testCase.id and self.respostaAlgoritmo == other.respostaAlgoritmo

    def toJson(self):
        return {
            "id":self.id,
            "testCaseId":self.testCase.id,
            "respostaAlgoritmo":self.respostaAlgoritmo,
            "status":self.status
        }

    
    def save(self):
        # verificar se já existe um resultadoTestCase com esse id
        resultadoTestCase = ResultadoTestCase.listAllByQuery(Query("testCaseId", "==", self.testCase.id))
        if len(resultadoTestCase) > 0:
            self.id = resultadoTestCase[0].id
        
        super().save()
        
        # se já existir, então usa esse id no objeto que será salvo
        # se não existir, salva um novo