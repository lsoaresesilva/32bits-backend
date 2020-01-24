import re

from letscode.model.errors.erroProgramacaoError import ErroProgramacaoError

class ErroProgramacao():
    def __init__(self, erro):
        self.texto = erro
        self.tipo = ""
        self.linha = 0
        
    def possuiErroVisualizacao(self):
        tipoErro = re.findall("([a-zA-Z]+)Error:", self.texto)
        if tipoErro:
            return True
        return False

    def possuiErroExecucao(self):
        
        linha = re.findall("line ([0-9]+)", self.texto)
        tipoErro = re.findall("([a-zA-Z]+Error):", self.texto) # TODO: ver a necessidade de mudar o código para ficar igual ao de cima: ...Error
        
        erro = False

        if tipoErro and linha:
            if(len(tipoErro) == 1) and (len(linha) == 1):
                self.tipo = tipoErro[0]
                self.linha = linha[0]
                erro = True
            else:
                erro = True

        return erro
