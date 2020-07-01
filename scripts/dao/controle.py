#Autor:Diego Silva
#Data:24/05/2020
#Descrição: Script para cadastros e consultas em banco de dados

from scripts.dao.banco import *
from scripts.dao.notascortereliga import *
from scripts.dao.statusdispositivocampo import *
#constantes , dados de acesso ao servidor de banco
HOST='localhost'
PORT=27017

#objetos de acesso ao banco de dados e interação com banco
COMUNICABANCO = MongoDBConexao(HOST,PORT)
CONTROLENOTA = DispositivoNotas()
CONTROLESTATUS = DispositivoStatus()

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
            return {'mensagem':'Ja existe uma nota cadastra para este dispositivo'}

    #metódo para consultar todas as notas cadastradas
    def todasAsNotas(self):
        return CONTROLENOTA.consultaTodasAsNotas(COMUNICABANCO.getConexaoMongo())

    #metódo para dispositivo em campo verificar se tem nota de corte e religa
    def notaDispositivo(self, payload):
        nota = CONTROLENOTA.consultaNotaDispositivo(COMUNICABANCO.getConexaoMongo(),payload)
        CONTROLENOTA.removerNota(COMUNICABANCO.getConexaoMongo(),payload)
        return nota

    #método para atualização de status do dispositivo
    def statusDispositivo(self, payload):
        device = {'device':payload['device']}
        statusatual = CONTROLESTATUS.consultaStatusAtual(COMUNICABANCO.getConexaoMongo(), device)

        #verifica se ja existe um status
        if statusatual is None:
            CONTROLESTATUS.insertStatus(COMUNICABANCO.getConexaoMongo(), payload)#apenas faz insert
        else:
            CONTROLESTATUS.removeUltimoStatus(COMUNICABANCO.getConexaoMongo(), device)#remove ultimo status
            CONTROLESTATUS.insertStatus(COMUNICABANCO.getConexaoMongo(), payload)#inser status atual

    #metodo para retornar todos os status
    def todosOsStatus(self):
        return CONTROLESTATUS.consultaStatus(COMUNICABANCO.getConexaoMongo())

    #consulta status de um dispositivo especifico
    def dispositivoStatus(self, payload):
        return CONTROLESTATUS.consultaStatusAtual(COMUNICABANCO.getConexaoMongo(), payload)
        
        
        
            
            
        

