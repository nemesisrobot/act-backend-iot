#Autor:Diego Silva
#Data:14/08/2020
#Descrição:Script de teste para o endpoint de cadatro de dispositivo

import requests as rq
import json

#definindo cabeçalho
HEADER = {'content-type':'application/json'}

#url da aplicacao


#metodo para consulta de dispositivo
def consultaexcluit(url):
    dados = rq.get(url=url)
    print(dados.status_code)
    print(dados.content)

#método para testes de cadastro e atualização
def cadeatu(payload, url):
    dados = rq.post(url=url, data=json.dumps(payload), headers=HEADER)    
    print(dados.status_code)
    print(dados.content)

    
#dados de envio para cadstro
payload = {    
    'device':'DOM2',
    'client':'Drone Tecnologia da Informação',
    'address':'rua Teste',
    'description':'cooworking'
}
cadeatu(payload,'http://192.168.15.15:5000/dispositivocadastraatualiza/CADASTRA')

payload = {
    
    'device':'XXXXXXXXXXXXXXXXXXX',
    'client':'mixxi',
    'address':'rua catuti',
    'description':'building'#,
    #'key':'50001805552501O5001551M80'
 }
cadeatu(payload,'http://192.168.15.15:5000/dispositivocadastraatualiza/CADASTRA')
#cadeatu(payload,'http://192.168.15.15:5000/dispositivocadastraatualiza/ATUALIZA')
#cadeatu(payload,'http://192.168.15.15:5000/dispositivocadastraatualiza/ATUdALIZA')

#consultaexcluit('http://192.168.15.15:5000/dispositivoconsultaexclui/EXCLUIR/XXXXXXXXXXXXXXXXXXX')
#consultaexcluit('http://192.168.15.15:5000/dispositivoconsultaexclui/EXCLUIR/Delta')

consultaexcluit('http://192.168.15.15:5000/dispositivobuscatodos')
