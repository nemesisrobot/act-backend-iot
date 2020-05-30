#Autor:Diego Silva
#Data:24/05/2020
#Descrição: Script para cadastros e consultas em banco de dados

from scripts.dao.banco import *
from scripts.dao.notascortereliga import *

#constantes , dados de acesso ao servidor de banco
HOST='localhost'
PORT=27017

#objetos de acesso ao banco de dados e interação com banco
COMUNICABANCO = MongoDBConexao(HOST,PORT)
CONTROLENOTA = DispositivoNotas()

#classe para realiza operações no banco de dados
class OperacoesBanco:

    #meto para cadastro de notas
    def cadastroNota(self, payload):

        #monta json de consulta banco
        device = {'device':payload['device']}

        #faz consulta por dispositivo
        existeembanco = CONTROLENOTA.consultaNotaDispositivo(COMUNICABANCO.getConexaoMongo(), device)

        #se não tiver nota cadastra sistema faz novo cadastro
        if existeembanco is None:
            return CONTROLENOTA.insertNotas(COMUNICABANCO.getConexaoMongo(),payload)

        #senão retorna mensagem dizendo que já existe nota
        else:
            return {'mensagem':'Já existe Uma nota'}

    #metódo para consultar todas as notas cadastradas
    def todasAsNotas(self):
        return CONTROLENOTA.consultaTodasAsNotas(COMUNICABANCO.getConexaoMongo())

    #metódo para dispositivo em campo verificar se tem nota de corte e religa
    def notaDispositivo(self, payload):
        nota = CONTROLENOTA.consultaNotaDispositivo(COMUNICABANCO.getConexaoMongo(),payload)
        CONTROLENOTA.removerNota(COMUNICABANCO.getConexaoMongo(),payload)
        return nota

