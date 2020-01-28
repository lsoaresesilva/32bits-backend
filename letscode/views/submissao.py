from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.http import JsonResponse

from firebase_admin import credentials
from firebase_admin import firestore
import firebase_admin

from letscode.model.testCase import TestCase
from letscode.model.juiz import Juiz
from letscode.model.submissao import Submissao

from letscode.model.arquivoSubmissao import ArquivoSubmissao
from letscode.model.errors.juizError import JuizError

from letscode.model.firestore.query import Query

import json
import os


class SubmissaoView(APIView):

    def post(self, request, format=None):
        
        json = "" 
        httpStatus = 201
        try:
            
            if Submissao.validarJson(request.data):
                
                submissao = Submissao.fromJson(request.data)

                juiz = Juiz(submissao)
                arquivo = ArquivoSubmissao(submissao.codigo)

                if request.data["tipo"] == "visualização":
                    json = juiz.executarVisualizacao(arquivo)
                else:
                    if request.data["tipo"] == "testes":
                        submissao.resultadosTestsCases = juiz.executarTestes(arquivo)
                    submissao.saida = juiz.executar(arquivo)
                    json = submissao.toJson()
            else:    
                httpStatus = 400
        except Exception as exception:
            json = {"mensagem":str(exception)}
            httpStatus = 500
        finally:
            if arquivo != None:
                arquivo.apagarArquivo()
            return JsonResponse(json, safe=False, status=httpStatus)


    @staticmethod
    def limparSaida(saida):
        pass