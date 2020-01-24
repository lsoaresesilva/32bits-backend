
from letscode.model.submissao import Submissao
from letscode.model.resultadoTestCase import ResultadoTestCase
from letscode.model.testCase import TestCase

import unittest

class TestSubmissao(unittest.TestCase):

    def test_deve_criar_objeto_de_json(self):
        json = {
            "submissao":{
                "algoritmo"
            },
            "resultados":[{"id":"1", "testCaseId":"2", "respostaAlgoritmo":"3", "status":True}, {"id":"2", "testCaseId":"1", "respostaAlgoritmo":"3", "status":False}],
            "saida":[]
        }
    
    def test_deve_gerar_json(self):
        s = Submissao(None, None, None, None)
        r1 = ResultadoTestCase(s, TestCase("2", [2], 2), "3", True)
        r1.id = "1"
        r2 = ResultadoTestCase(s, TestCase("1", [2], 2), "3", False)
        r2.id = "2"
        resultados = [r1, r2]
        s.resultadosTestsCases = resultados
        json = {
            "id":s.id,
            "resultados":[{"id":"1", "testCaseId":"2", "respostaAlgoritmo":"3", "status":True}, {"id":"2", "testCaseId":"1", "respostaAlgoritmo":"3", "status":False}],
            "saida":[]
        }

        submissaoJson = s.toJson()

        self.assertDictEqual(json, submissaoJson)