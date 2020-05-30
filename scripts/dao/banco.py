#Autor:Diego Silva
#Data:25/05/2020
#Descrição: script para comunicação com banco de dados

from pymongo import MongoClient

#classe mãe para atributos de acesso a banco
class ConexaoBanco:
    def __init__(self, servidor, porta):
        self.__servidor = servidor
        self.__porta = porta

    #metódo para retorno de dados de servidor
    def getServidor(self):
        return self.__servidor

    #metódo para retorno de dados da porta
    def getPorta(self):
        return self.__porta

#classe filha de ConexaoBanco
class MongoDBConexao(ConexaoBanco):
    def __init__(self, servidor, porta):
        super(MongoDBConexao, self).__init__(servidor, porta)

    def getConexaoMongo(self):
        conexao = MongoClient(self.getServidor(),self.getPorta())
        db = conexao.dispositivos
        return db
