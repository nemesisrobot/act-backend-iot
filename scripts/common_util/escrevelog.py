#Autor:Diego Silva
#Data:15/08/2020
#Descrição:Scriptp para escrita de logs do sistema
import datetime
class EscreveLogSistema:
	def __init__(self, arquivo):
		self._arquivo = arquivo

		#metodo para escrever em log
	def escreve(self, conteudo):
		escreverlog = open(self._arquivo,'a+')
		escreverlog.write('[{}]:{}'.format(str(datetime.datetime.now()),str(conteudo)))
		escreverlog.write('\n')
		escreverlog.close()