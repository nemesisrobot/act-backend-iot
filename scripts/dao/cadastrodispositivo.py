#Autor:Diego Silva
#Data:13/08/2020
#Descrição:Script para operações em banco sobre o cadastro de dispositivos

#classe mãe para controle básicos de cadastros
class Cadastra:

	def __init__(self, conexao):
		self._conexao = conexao

	def getinsertDispositivo(self, dadoscadastro):
		resultadoCadastro = self._conexao.dispositivocadastro.insert_one(dadoscadastro)
		return resultadoCadastro.inserted_id

	def getprocuraDispositivo(self, dadoscadastro):
		buscadispositivo = self._conexao.dispositivocadastro.find_one(dadoscadastro)
		return buscadispositivo

	def getatualizaDispositivo(self, dispositivo , dadoscadastro):
		self._conexao.dispositivocadastro.update_one(dispositivo, dadoscadastro)


	def removeDispositivo(self, dadoscadastro):
		self._conexao.dispositivocadastro.delete_one(dadoscadastro)

	def getDipositivos(self):
		return self._conexao.dispositivocadastro.find()

#classe Responsavel pelo cadastro de dispositivos
class  CadastraDipositivo(Cadastra):
	def __init__(self, conexao):
		super(CadastraDipositivo, self).__init__(conexao)


	#método para adicionar dispositovo no banco de dados
	def adicionaDispositivo(self, dadoscadastro):		
		if(self.getprocuraDispositivo({'device':dadoscadastro['device']}) is None):
			print(self.getinsertDispositivo(dadoscadastro))
			return '{}'.format(dadoscadastro['key'])
		else:
			return 'Dispositivo Ja cadastrado'

	#método para atualizar dados em banco
	def atualizaDispositivo(self, dadoscadastro):
		self.getatualizaDispositivo({'key':dadoscadastro['key']}, {"$set":dadoscadastro})
		return 'Dados do dispositivo atualizados com sucesso'

	def pesquisaDispositivo(self, dadoscadastro):
		if(self.getprocuraDispositivo(dadoscadastro) is None):
			return 'Dispositivo Nao Localizado'
		else:
			return self.getprocuraDispositivo(dadoscadastro)

	def deletaDispositivo(self, dadoscadastro):
		self.removeDispositivo(dadoscadastro)
		return 'Dispositivo deletado com sucesso'

	def pesquisaTodosDipositivos(self):
		return self.getDipositivos()
		
