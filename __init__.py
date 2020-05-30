#Autor:Diego Silva
#Data:24/05/2020
#Descrição:Script responsavel por micro serviço
from sys import path
path.append('/scripts')
from flask import Flask, request, jsonify
from scripts.dao.controle import OperacoesBanco
import datetime


#lista de notas
listanotas = []

#constante de controle de banco
OPERACAO = OperacoesBanco()

#criando objote para trabalho com endpoinst
app = Flask(__name__)

#metodo para escrever em log
def escreve(conteudo):
    escreverlog = open('logs/servidor.log','a+')
    escreverlog.write('[{}]:{}'.format(str(datetime.datetime.now()),str(conteudo)))
    escreverlog.write('\n')
    escreverlog.close()
    
#end-point para cadastra notas
@app.route('/notaservico', methods = ['POST'])
def cadastrodenotas():
    escreve('Cadastrando Nova nota de corte e religa')
    novanota = request.get_json()
    payload = {
           'device':novanota['device'],
           'corte':novanota['corte'],
           'data':novanota['data']
        }
    escreve('Json recebido {}'.format(str(payload)))
    resposta = str(OPERACAO.cadastroNota(payload))
    
    if 'nota' in resposta:
        escreve('Resposta {}'.format(str(resposta)))
        return jsonify(resposta)
    else:
        escreve('Resposta {}'.format(str({'Mensagens': 'OK', 'Codigo':resposta})))
        return jsonify ({'Mensagens': 'OK', 'Codigo':resposta}), 201

#end-point para consultar todas as notas
@app.route('/notaservico', methods = ['GET'])
def todasAsNotasCadastradas():
    listanotas.clear()
    escreve('Consultando todas as notas da base')
    notas = OPERACAO.todasAsNotas()
    for x in notas:
        print({'device':x['device'], 'corte':x['corte'], 'data':x['data']})
        listanotas.append({'device':x['device'], 'corte':x['corte'], 'data':x['data']})
    return jsonify(listanotas)

#end-point para dispositivo consultar nota
@app.route('/notaservico/<string:device>', methods = ['GET'])
def notaDispositivo(device):
    #monta payloda para busca de nota
    payload = {'device':str(device)}
    escreve('Dispositivo {}, procurando por nota'.format(str(payload)))
    sem_nota = {'device':3, 'corte':3, 'data':3}
    
    respotadevice = OPERACAO.notaDispositivo(payload)
    if respotadevice is None:
        escreve('Sem nota de corte e religa')
        return jsonify(sem_nota)
    else:
        escreve('Nota encontrada')
        escreve('Device: {}'.format(respotadevice['device']))
        return jsonify({'device':respotadevice['device'], 'corte':respotadevice['corte'], 'data':respotadevice['data']})
    
if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000)
