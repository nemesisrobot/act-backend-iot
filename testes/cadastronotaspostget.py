import requests as rq
import json


#cabeçalho padrão
headers = {'content-type':'application/json'}
#links de acesso para cadastros notaas
linkdevice1 = 'http://192.168.15.15:5000/notaservico'

payload = {'device':'xpto1','corte':0,'data':'20/04/2020 10:10:10'}
#teste de post no webservice
dados = rq.post(url=linkdevice1, data=json.dumps(payload), headers=headers)
print(str(dados.status_code))
print(str(dados.content))
#dados = rq.get(url=linkdevice1)
#print(str(dados.status_code))
#print(str(dados.content))
