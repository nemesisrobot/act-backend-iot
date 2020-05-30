#Autor:Diego Silva
#Data:30/05/2020
#Descrição:Script com procedimentos para status do device

class DispositivoStatus:

    #metódo para inserir status do dispositivo
    def insertStatus(self, conexao, statusatual):
        conexao.statusdispositivo.insert_one(statusatual)

    #metódo que procura por status do dispostivo
    def consultaStatusAtual(self, conexao, dispositivo):
        return conexao.statusdispositivo.find_one(dispositivo)


    #metódo para remoção do status atual
    def removeUltimoStatus(self, conexao, dispositivo):
        conexao.statusdispositivo.delete_one(dispositivo)

    #metodo consulta todos os status
    def consultaStatus(self, conexao):
        #pegando tos os status
        dadosstatusbusca = conexao.statusdispositivo.find()
        return list(dadosstatusbusca)
        
