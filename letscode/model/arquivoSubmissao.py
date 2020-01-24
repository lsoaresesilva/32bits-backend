import random
import string
import os

from letscode.model.errors.arquivoSubmissaoError import ArquivoSubmissaoError


class ArquivoSubmissao():

    def __init__(self, algoritmo):
        
        if type(algoritmo) == str and algoritmo != "":
            self.arquivo = self.criarArquivo()
            self.escreverCodigoNoArquivo(algoritmo)
        else:
            raise ValueError("Algoritmo não pode estar vazio.")

    def criarArquivo(self):
        nomeArquivo = self.gerarNomeArquivo()
        arquivo = open(nomeArquivo,"w+")

        return arquivo

    def nome(self):
        return self.arquivo.name

    def apagarArquivo(self):
        #TODO: verificar se o arquivo existe
        if self.arquivo != None:
            self.arquivo.close()
            try:
                os.remove(os.path.realpath(self.arquivo.name))
                self.arquivo = None
            except (OSError):
                print("disparou")

    def is_arquivo_valido(self):
        # TODO: verificar se o arquivo existe
        if self.arquivo == None:
            return False

        return True
    
    def escreverCodigoNoArquivo(self, algoritmo):

        algoritmo = algoritmo.split("\n")

        for linha in algoritmo:
            
            # TODO: verificar antes se o arquivo está aberto
            self.arquivo.write(linha+"\n")

        self.arquivo.flush()
        os.fsync(self.arquivo.fileno())
        self.arquivo.close()
        
        # necessário, pois o flush do python não estava escrevendo no arquivo a tempo
        self.arquivo = open(self.arquivo.name,"r")
        

        return True

    # obtido em: https://stackoverflow.com/questions/2257441/random-string-generation-with-upper-case-letters-and-digits-in-python
    def gerarNomeArquivo(self, size=6, chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))+".py"