#Autor:Diego Silva
#Data:24/05/2020
#Descrição:Script para interação com coleção das notas dispositivos

#classe para trabalhar com interação com coleção do mongodb
class DispositivoNotas:

    #metódo para cadastrar nota de corte e religa
    def insertNotas(self, conexao, nota):
        resultado = conexao.notas.insert_one(nota)
        return resultado.inserted_id

    #metódo para consulta de todas as notas em base
    def consultaTodasAsNotas(self, conexao):
        #pegando dados da coleção
        dadosbusca = conexao.notas.find()
        return list(dadosbusca)

    #metódo para consultar nota para o dispositivo
    def consultaNotaDispositivo(self, conexao, dispositivo):
        buscadispositivo = conexao.notas.find_one(dispositivo)
        return buscadispositivo

    #metódo que remove nota do banco
    def removerNota(self, conexao, dispositivo):
        conexao.notas.delete_one(dispositivo) 
        
