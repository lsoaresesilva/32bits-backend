import pexpect
import re
import os

from letscode.model.errors.juizError import JuizError
from letscode.model.testCase import TestCase
from letscode.model.resultadoTestCase import ResultadoTestCase
from letscode.model.submissao import Submissao
from letscode.model.erroProgramacao import ErroProgramacao
from letscode.model.errors.erroProgramacaoError import ErroProgramacaoError


# Realiza diferentes operações no código enviado pelo estudante, como execução, execução com testes cases e visualização de algoritmos.
class Juiz():

    def __init__(self, submissao):

        self.submissao = submissao

    # TODO: deve impedir que código maliciosos possam ser executados. desabilitar o uso de import os e outros.

    def validarCodigoMalicioso(self):
        pass

    def isQuestaoValida(self):
        if type(self.submissao) == Submissao:
            raise JuizError("Uma questão precisa ser informada")

    # Formata os inputs que serão utilizados na visualização do algoritmo.
    def prepararInputs(self, entradas):
        inputs = ""

        for entrada in entradas:
            # Verificar se é um número
            numeroApenas = re.search("^[0-9]*$", entrada)
            if numeroApenas != None:
                inputs += entrada+","
            else:
                inputs += '"'+entrada+'"'+','

        inputs = inputs[:-1]  # remove a , que foi acrescentada a mais.

        return "'["+inputs+"]'"

    # Constrói um trace de execução para o algoritmo do estudante.
    # Utiliza códigos da biblioteca PythonTutor.
    def executarVisualizacao(self, arquivo):
        jsonTrace = ""

        teste = self.submissao.questao.testsCases[0]
        if teste != None:
            inputs = self.prepararInputs(teste.entradas)
        # TODO: colocar tudo dentro do if, se n tiver teste, n tem como visualizar.

        if arquivo.is_arquivo_valido():
            #if self.matchInputCodigo(teste["entradas"]):
            path = os.path.dirname(os.path.realpath(__file__))
            path = path+'/pythontutor/generate_json_trace.py'
            comando = 'python3 '+path+' '+arquivo.nome()+' -i '+inputs
            # BUG: tem de recuperar o dir do projeto.. para poder executar
            child = pexpect.spawn(
                'python3 '+path+' '+arquivo.nome()+' -i '+inputs)
            child.expect(pexpect.EOF)
            jsonTrace = child.before.decode("utf-8")
            erro = ErroProgramacao(jsonTrace)
            if erro.possuiErroVisualizacao() == False:
                return jsonTrace
            else:
                raise JuizError(
                    "O código apresentou o seguinte erro '"+erro.tipo)

            #else:
            #    raise JuizError(
            #        "A quantidade de inputs em seu código é menor/maior que a quantidade de entradas")
        else:
            raise JuizError("O arquivo de código não foi encontrado.")

        return jsonTrace

    # Execução de código python em que não há testscases
    def executar(self, arquivo):

        if arquivo.is_arquivo_valido():
            
            msgRetornoAlgoritmo = ""
            if len(self.submissao.questao.testsCases) > 0:
                for teste in self.submissao.questao.testsCases:

                    child = pexpect.spawn('python3 '+arquivo.nome())
                    for entradas in teste.entradas:
                        child.expect(".*")
                        child.sendline(entradas)

                    child.expect(pexpect.EOF)
                    msgRetornoAlgoritmo = child.before.decode("utf-8")
                    break
                
                return self.obterSaidaAlgoritmo(msgRetornoAlgoritmo, self.submissao.questao.testsCases[0].entradas)
            else:
                child = pexpect.spawn('python3 '+arquivo.nome())
                child.expect(pexpect.EOF)
                msgRetornoAlgoritmo = child.before.decode("utf-8")
                return msgRetornoAlgoritmo
        else:
            raise JuizError("O arquivo de código não foi encontrado.")

    # Executa o código do estudante comparando-o à testscases de uma questão.
    def executarTestes(self, arquivo):
        resultados = []
        resultadoTeste = False
        msgRetornoAlgoritmo = ""

        for teste in self.submissao.questao.testsCases:
            if arquivo.is_arquivo_valido():
                #if self.matchInputCodigo(teste["entradas"]):

                child = pexpect.spawn('python3 '+arquivo.nome())

                try:

                    for entradas in teste.entradas:
                        child.expect(".*")
                        child.sendline(entradas)

                    child.expect(pexpect.EOF)
                    msgRetornoAlgoritmo = child.before.decode("utf-8")
                    try:
                        erro = ErroProgramacao(msgRetornoAlgoritmo)
                        if erro.possuiErroExecucao():
                            raise JuizError(
                                "O código apresentou o seguinte erro '"+erro.tipo+"' na linha "+erro.linha)
                        else:  # Não há erro, verificar o resultado test de testcase normalmente
                            
                            resultadoTeste = self.compararSaidaEsperadaComSaidaAlgoritmo(
                                msgRetornoAlgoritmo, teste.saida)
                    finally:
                        child.close()
                except OSError as e:
                    # TODO: melhorar a mensagem para indicar qual o problema
                    raise JuizError("O código possui um erro."+e)

                #else:
                #    raise JuizError(
                #        "A quantidade de inputs em seu código é menor que a quantidade de entradas")

                resultado = ResultadoTestCase(None, teste, self.obterSaidaAlgoritmo(
                    msgRetornoAlgoritmo, teste.entradas), resultadoTeste)

                resultados.append(resultado)
            else:
                raise JuizError("O arquivo de código não foi encontrado.")

        # self.salvarResultados(resultados) # migrou para o frontend que será responsável por salvar tudo

        return resultados

    def salvarResultados(self, resultados):
        # TODO: usar transaction, para salvar apenas se todos forem salvos.
        for resultado in resultados:
            resultado.save()

    def obterTextosInput(self):

        textosInput = []
        inputs = re.findall("input\((.*[^\(\)])\)", self.submissao.codigo)
        if inputs and len(inputs) > 0:
            for textoInput in inputs:

                textoInput = textoInput.replace("'", "")
                textoInput = textoInput.replace('"', "")

                textosInput.append(textoInput)

        return textosInput

    # O output do algoritmo é constituído pelas entradas de uma questao e do que foi impresso com print. Essa função remove as entradas dessa saída
    def retirarEntradasDoOutput(self, resultadoAlgoritmo, entradas):

        saidas = resultadoAlgoritmo.splitlines()
       
        for entrada in entradas:
            for saida in saidas:
                if entrada == saida:
                    saidas.remove(entrada)
                    break
        
        return saidas


    def obterSaidaAlgoritmo(self, resultadoAlgoritmo, entradas):

        textosInput = self.obterTextosInput()

        
        #saidas = resultadoAlgoritmo.splitlines()
        saidas = self.retirarEntradasDoOutput(resultadoAlgoritmo, entradas)
        entradasRemovidas = []

        outputAlgoritmo = []
        for saida in saidas:
            # Se for um texto que apareceu em razão da entrada do test case ou do input do algoritmo, deve ignorar
            textoEntradaInput = False
            for textoInput in textosInput:  # OU se for uma das entradas do testcase, também ignorar
                if textoInput != "":
                    if textoInput in saida:
                        textoEntradaInput = True
                        break
            #for textoEntrada in entradas:  # OU se for uma das entradas do testcase, também ignorar
            #    if textoEntrada == saida and saida not in entradasRemovidas:
            #        textoEntradaInput = True
            #        entradasRemovidas.append(textoEntrada)
            #        break

            if not textoEntradaInput:
                saida = self.converterParaDuasCasasDecimaisFloat(saida)
                outputAlgoritmo.append(saida)

        if len(outputAlgoritmo) > 0:
            return outputAlgoritmo[0]
        else:
            return outputAlgoritmo

    def compararSaidaEsperadaComSaidaAlgoritmo(self, resultadoAlgoritmo, resultadoEsperado):
        algoritmoCorreto = False

        saidas = resultadoAlgoritmo.splitlines()
        for texto in saidas:
            texto = self.converterParaDuasCasasDecimaisFloat(texto)
            if texto == resultadoEsperado: # TODO: Fazer a comparação para ignorar diferenças após 1 casa decilmal.
                algoritmoCorreto = True
                break

        return algoritmoCorreto

    # Verifica se o código dispõe do quantitativo de inputs necessários para a quantidade de entradas
    def matchInputCodigo(self, entradas):
        totalInputs = re.findall("input", self.submissao.codigo)

        if len(entradas) == len(totalInputs):
            return True
        return False

    def converterParaDuasCasasDecimaisFloat(self, saida):
        if len(re.findall("[0-9]+\.[0-9]+", saida)) > 0: # Apenas converterá se for float.
            saida = float(saida)
            saida = round(saida, 2)
            saida = str(saida)
        return saida

