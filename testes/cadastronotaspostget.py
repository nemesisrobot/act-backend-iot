import requests as rq
import json
import ast

#cabeçalho padrão
headers = {'content-type':'application/json'}
#links de acesso para cadastros notaas
linkdevice1 = 'http://192.168.15.15:5000/notaservico'

payload = {'device':'xpto1','corte':0,'data':'30/06/2020 10:10:10'}
#teste de post no webservice
dados = rq.post(url=linkdevice1, data=json.dumps(payload), headers=headers)
print(str(dados.status_code))
print(str(dados.content))


mensagem = (dados.content).decode()
mensagem = mensagem.replace('\n','')

print('------string--------')
print(mensagem)
dicionario = ast.literal_eval(mensagem)
dicionario = ast.literal_eval(dicionario)
print('------dicionario--------')
print(type(dicionario))
print(dicionario['mensagem'])
#dados = rq.get(url=linkdevice1)
#print(str(dados.status_code))
#print(str(dados.content))
