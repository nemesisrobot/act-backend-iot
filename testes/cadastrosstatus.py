import requests as rq
import json
import time

#cabeçalho padrão
headers = {'content-type':'application/json'}
#links de acesso para cadastros notaas
linkdevice1 = 'http://192.168.15.15:5000/dispositivostatus'

payload = {'device':'xpto3','corte':1}
payload1 = {'device':'xpto1','corte':0}

def teste(payload):
    dados = rq.post(url=linkdevice1, data=json.dumps(payload), headers=headers)
    print(str(dados.status_code))
    print(str(dados.content))


teste(payload)
time.sleep(5)
teste(payload1)
