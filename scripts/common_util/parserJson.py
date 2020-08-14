#Autor:Diego Silva
#Data:14/08/2020
#Descrição:Script para fazer parser de dados 


#classe mãe que recebe dado puro enviado pelo front end
class MensagemJson:

	def __init__(self, json):
		self._json = json

	def getJson(self):
		return self._json

#classe para fazer parser das mensagens de cadastro do dispositivo
class ParserCadastroDispositivo(MensagemJson):
	def __init__(self, json):
		super(ParserCadastroDispositivo, self).__init__(json)

	#método para fazer parser de mensagem e compor json de cadastro
	def getJsonCadastroDispositivo(self, chave):

		#pega dados enviados por usuário e monta json
		return {
			'device':self.getJson()['device'],
			'client':self.getJson()['client'],
			'address':self.getJson()['address'],
			'description':self.getJson()['description'],
			'key':chave.getChaveDispositivo()
		}


	def getJsonAtualizaDispositivo(self):
		#parser dos dados de atualização
		return {
			'device':self.getJson()['device'],
			'client':self.getJson()['client'],
			'address':self.getJson()['address'],
			'description':self.getJson()['description'],
			'key':self.getJson()['key']
		}


	#método compõe json de busca para dispositivo
	def getJsonBuscaDispositivo(self):
		return {'device':self.getJson()}

	#compõe de json de retorno removendo camo _Id
	def removerSereliziacao(self, dadobanco):

		#trativa caso venha alguam mensagen diferente do que um dado do tipo diconário
		try:
			return {
				'device':dadobanco['device'],
				'client':dadobanco['client'],
				'address':dadobanco['address'],
				'description':dadobanco['description'],
				'key':dadobanco['key']
			}
		except:
			#retorna mensagem pura
			return dadobanco

	def getTodosOsDispositivos(self, dadobanco):
		listadispositivos = []

		try:
			#faz append de dados para lista e retorna todos os dados
			for dado in dadobanco:
				listadispositivos.append(
					{
						'device':dado['device'],
						'client':dado['client'],
						'address':dado['address'],
						'description':dado['description'],
						'key':dado['key']
					})

			return listadispositivos
		except:
			return {'Mensagem':'Nenhum Dipositivo Localizado!!!'}
