import re

from letscode.model.errors.erroProgramacaoError import ErroProgramacaoError

class ErroProgramacao():
    def __init__(self, erro):
        self.texto = erro
        self.tipo = None
        self.linha = None
        self.getErrorData(erro)
        
    """
    def getErrorData(self, erro):
        linha = re.findall("line ([0-9]+)", self.texto)
        tipo = re.findall("([a-zA-Z]+Error):", self.texto) # TODO: ver a necessidade de mudar o código para ficar igual ao de cima: ...Error

        if tipo and linha:
            if(len(tipo) == 1) and (len(linha) == 1):
                self.tipo = tipo[0]
                self.linha = linha[0]
                erro = True
            else:
                erro = True

    def possuiErroVisualizacao(self):
        tipoErro = re.findall("([a-zA-Z]+)Error:", self.texto)
        if tipoErro:
            return True
        return False
    """
    @staticmethod
    def possuiErroExecucao(erro):
        
        linha = re.findall("line ([0-9]+)", erro)
        tipo = re.findall("([a-zA-Z]+Error):", erro) # TODO: ver a necessidade de mudar o código para ficar igual ao de cima: ...Error

        if tipo and linha:
            if(len(tipo) == 1) and (len(linha) == 1):
                return True

        return False

