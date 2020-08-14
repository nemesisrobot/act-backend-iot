#Autor:Diego Silva
#Data:13/08/2020
#Descrição:Scrip para gerar chave unica de para o dispositivo

import string
import random
import datetime

#classe geradora da chave unica do dispositivo
class GeradoraDeChave:

	#construtor para inicializar atributos
	def __init__(self, dispositivo, tamanhochave):
		self._dispositivo = dispositivo
		self._tamanhochave = tamanhochave

	#método gerador da chave
	def getChaveDispositivo(self):
		data = (((str(datetime.datetime.now()).replace(' ','')).replace('-','')).replace('.','')).replace(':','')
		novachave = '{}{}'.format(data,self._dispositivo.upper())
		return ''.join(random.choice(novachave) for _ in range(self._tamanhochave))