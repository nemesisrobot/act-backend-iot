#Autor:Diego Silva
#Data:24/05/2020
#Descrição:Script responsavel por micro serviço
from sys import path
path.append('/scripts')
from flask import Flask, request, jsonify
from scripts.dao.controle import OperacoesBanco
from scripts.common_util.geradorchave import GeradoraDeChave
from scripts.common_util.parserJson import *
from scripts.common_util.escrevelog import *
import datetime

#instanciando classe para escrita de log
log = EscreveLogSistema('logs/servidor.log')

#lista de notas
listanotas = []
listastatus = []

#constante de controle de banco
OPERACAO = OperacoesBanco()

#Constante para a chave geradora
TAMANHOCHAVE = 25


#criando objote para trabalho com endpoinst
app = Flask(__name__)


    
#end-point para cadastra notas
@app.route('/notaservico', methods = ['POST'])
def cadastrodenotas():
    log.escreve('Cadastrando Nova nota de corte e religa')
    novanota = request.get_json()
    payload = {
           'device':novanota['device'],
           'corte':novanota['corte'],
           'data':novanota['data']
        }
    log.escreve('Json recebido {}'.format(str(payload)))
    resposta = str(OPERACAO.cadastroNota(payload))
    
    if 'nota' in resposta:
        log.escreve('Resposta {}'.format(str(resposta)))
        return jsonify(resposta), 400
    else:
        log.escreve('Resposta {}'.format(str({'Mensagens': 'OK', 'Codigo':resposta})))
        return jsonify ({'Mensagens': 'OK', 'Codigo':resposta}), 201

#end-point para consultar todas as notas
@app.route('/notaservico', methods = ['GET'])
def todasAsNotasCadastradas():
    listanotas.clear()
    log.escreve('Consultando todas as notas da base')
    notas = OPERACAO.todasAsNotas()
    for x in notas:
        print({'device':x['device'], 'corte':x['corte'], 'data':x['data']})
        listanotas.append({'device':x['device'], 'corte':x['corte'], 'data':x['data']})
    return jsonify(listanotas)

#endpoint para consulta uma nota apenas
@app.route('/notaservicounica/<string:device>')
def notaDispositivoUnica(device):
    #procurando por nota
    parsernotas = ParserNotasServico(None)
    nota = OPERACAO.consultaNotaUnica(parsernotas.getDispositivo(device))
    log.escreve(nota)
    return jsonify(parsernotas.getTrataNota(nota))


#end-point para dispositivo consultar nota
@app.route('/notaservico/<string:device>', methods = ['GET'])
def notaDispositivo(device):
    #monta payloda para busca de nota
    payload = {'device':str(device)}
    log.escreve('Dispositivo {}, procurando por nota'.format(str(payload)))
    sem_nota = {'device':3, 'corte':3, 'data':3}
    
    respotadevice = OPERACAO.notaDispositivo(payload)
    if respotadevice is None:
        log.escreve('Sem nota de corte e religa')
        return jsonify(sem_nota)
    else:
        log.escreve('Nota encontrada')
        log.escreve('Device: {}'.format(respotadevice['device']))
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
    log.escreve('Atualizando status do device {}'.format(str(dispositivocampo['device'])))
    OPERACAO.statusDispositivo(payload)

    #retorna ok para device
    log.escreve('Respondendo com {}'.format(str(201)))
    return jsonify({'Mensagem':'ok'}),201
    
#end-point para retornar status de todos os dispositivos
@app.route('/dispositivostatus', methods=['GET'])
def todosOsStatusDispositivos():
    listastatus.clear()
    log.escreve('Checando status de todos os dispositivos')
    status = OPERACAO.todosOsStatus()
    for s in status:
        print({'device':s['device'], 'corte':s['corte'], 'data':s['data']})
        log.escreve(str({'device':s['device'], 'corte':s['corte'], 'data':s['data']}))
        listastatus.append({'device':s['device'], 'corte':s['corte'], 'data':s['data']})
    return jsonify(listastatus)

#end-point para consulta especifica de um unico dispositivo    
@app.route('/dispositivostatus/<string:device>', methods=['GET'])
def consultaStatusDispositivo(device):
    #montando dados
    payload = {'device':str(device)}
    sem_status = {'device':None, 'corte':None, 'data':None}

    #fazendo busca
    log.escreve('Dispositivo {}, procurando por status'.format(str(payload)))
    status = OPERACAO.dispositivoStatus(payload)

    if status is None:
        log.escreve('Dispositivo {}, sem status para esse dispositivo'.format(str(payload)))
        return jsonify(sem_status)
    else:
        log.escreve('Dispositivo {}, Status encontrado'.format(str(payload)))
        log.escreve('Dispositivo {}, status {}'.format(str(payload),(str(status['corte']))))
        return jsonify({'device':status['device'], 'corte':status['corte'], 'data':status['data']})

#endpoint para cadastro e atualziação de dados do dipositivo
@app.route('/dispositivocadastraatualiza/<string:tipo>', methods=['POST'])
def cadastraatualizadispositivo(tipo):

    #instância classe para fazer parser dos dados
   dadosdispositivo = ParserCadastroDispositivo(request.get_json())

   #operação de cadastro
   if(tipo=='CADASTRA'):
    log.escreve('Parser de mensagem Json')
    jsoncadastro = dadosdispositivo.getJsonCadastroDispositivo(GeradoraDeChave(request.get_json()['device'],TAMANHOCHAVE))
    
    log.escreve(jsoncadastro)
    novachave = OPERACAO.dispositivoCadastro(jsoncadastro)
   
    log.escreve('Cadastro: {}'.format(str(novachave)))
    return jsonify({'Mensagem':novachave})

   #operação de atualziação de dados
   elif(tipo=='ATUALIZA'):
    log.escreve('Atualizando dados do dispositivo')
    msg = OPERACAO.dispositivoAtualizacao(dadosdispositivo.getJsonAtualizaDispositivo())

    log.escreve('Atualização: {}'.format(str(msg)))
    return jsonify({'Mensagem':msg})

    #erro para tipo invalido
   else:
    log.escreve('Url não existe')
    return jsonify({'Mensagem':'Url nao existe'}),404

#end-point para consulda e exclusão de dispositivo
@app.route('/dispositivoconsultaexclui/<string:tipo>/<string:device>', methods=['GET'])
def dispositivopesquisaexclui(tipo, device):
    dispositivo = ParserCadastroDispositivo(device)
    if(tipo=='CONSULTA'):
        mensagem = dispositivo.removerSereliziacao(OPERACAO.dispositivoBusca(dispositivo.getJsonBuscaDispositivo()))
        log.escreve(mensagem)
        return jsonify(mensagem)
    elif(tipo=='EXCLUIR'):
        log.escreve('Deletano Disposivito')
        mensagem = OPERACAO.dispositivoDelete(dispositivo.getJsonBuscaDispositivo())
        log.escreve(mensagem)
        return jsonify({'Mensagem':mensagem})
    else:
        log.escreve('Url não existe')
        return jsonify({'Mensagem':'Url nao existe'}),404  

#end-point para consultar todos os dispositivos
@app.route('/dispositivobuscatodos', methods=['GET'])
def dispositivoBuscaTodos():
    dispositivo = ParserCadastroDispositivo(None)
    dispositivo = dispositivo.getTodosOsDispositivos(OPERACAO.dispositivoPegaTodos())
    log.escreve(dispositivo)
    return jsonify(dispositivo)

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000, debug=True)
