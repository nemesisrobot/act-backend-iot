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
listastatus = []

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
        return jsonify(resposta), 400
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

#end-point para atualização de status
@app.route('/dispositivostatus', methods=['POST'])
def atualizaStatusDispositivo():

    #pega dados de post
    dispositivocampo = request.get_json()

    #gera payload
    payload = {
        'device':dispositivocampo['device'],
        'corte':dispositivocampo['corte'],
        'data':str(datetime.datetime.now())
        }
    
    #executa procedimentos em base de dados
    escreve('Atualizando status do device {}'.format(str(dispositivocampo['device'])))
    OPERACAO.statusDispositivo(payload)

    #retorna ok para device
    escreve('Respondendo com {}'.format(str(201)))
    return jsonify({'Mensagem':'ok'}),201
    
#end-point para retornar status de todos os dispositivos
@app.route('/dispositivostatus', methods=['GET'])
def todosOsStatusDispositivos():
    listastatus.clear()
    escreve('Checando status de todos os dispositivos')
    status = OPERACAO.todosOsStatus()
    for s in status:
        print({'device':s['device'], 'corte':s['corte'], 'data':s['data']})
        escreve(str({'device':s['device'], 'corte':s['corte'], 'data':s['data']}))
        listastatus.append({'device':s['device'], 'corte':s['corte'], 'data':s['data']})
    return jsonify(listastatus)

#end-point para consulta especifica de um unico dispositivo    
@app.route('/dispositivostatus/<string:device>', methods=['GET'])
def consultaStatusDispositivo(device):
    #montando dados
    payload = {'device':str(device)}
    sem_status = {'device':None, 'corte':None, 'data':None}

    #fazendo busca
    escreve('Dispositivo {}, procurando por status'.format(str(payload)))
    status = OPERACAO.dispositivoStatus(payload)

    if status is None:
        escreve('Dispositivo {}, sem status para esse dispositivo'.format(str(payload)))
        return jsonify(sem_status)
    else:
        escreve('Dispositivo {}, Status encontrado'.format(str(payload)))
        escreve('Dispositivo {}, status {}'.format(str(payload),(str(status['corte']))))
        return jsonify({'device':status['device'], 'corte':status['corte'], 'data':status['data']})
    
    
if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000)
