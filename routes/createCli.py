from datetime import datetime
from flask import Blueprint, Response, request, jsonify

#primeiro vez criando algo do tipo em python então vamos lá ^^

def createClientBlueprint(db, Cliente): #funcao para fazer a criação da rota por fora do app.py
  createCliente = Blueprint('createCliente', __name__)  #criação do nome da blueprint
  @createCliente.route('/createCli', methods=['POST']) #criação da rota
  def create_cliente(): #funcionamento da rota
    statusTemp = 0 #setando status para retorno
    errorTemp = "null" #setando erro para retorno
    try:
      request_data = request.get_json(force=True) #aqui pega o JSON do postman ou do front end...
      nomeTemp = request_data['nome'] #seta nome para testes
      razaosoc = request_data['razao_social'] #seta razaosocial para testes
      cnpjTemp = request_data['cnpj'] #seta cnpj para testes
      if (nomeTemp == None or nomeTemp == ""): #se nome estiver vazio retorna erro de nome
        statusTemp = 400
        errorTemp = "Informe um nome válido"
      if (razaosoc == None or razaosoc == ""): #se razão social estiver vazia retorna erro
        statusTemp = 400
        errorTemp = "Informe uma razão social válida"
      else:         #caso razao social não seja nula verifica se não possui nenhuma igual no banco
        teste = Cliente.query.filter_by(razao_social=razaosoc).first()
        if (teste):     #se possuir alguma ja no banco retorna que ja está em uso
          statusTemp = 400
          errorTemp = "Razão social já em uso"
      if (cnpjTemp == None or cnpjTemp == "" or len(cnpjTemp)<14 or cnpjTemp == 0 or len(cnpjTemp)>18): #se CNPJ estiver vazio, for menor que 14 ou maior que 18 da erro
        statusTemp = 400
        errorTemp = "CNPJ inválido"
      else: #caso passe no if anterior se estiver no banco ja da erro também
        teste = Cliente.query.filter_by(cnpj=cnpjTemp).first()
        if (teste):
          statusTemp = 400
          errorTemp = "CNPJ já em uso"  # erro ^^
      if (statusTemp == 0): #se em nenhum momento deu erro durante a verificação passa para salvar no banco
        dataInclusao = datetime.now()  #como é data de inclusão entao ele pega a data da hora de inclusao para jogar no banco
        cliente = Cliente(nome=nomeTemp, razao_social=razaosoc, cnpj=cnpjTemp, data_inclusao=dataInclusao)  #cria o cliente para inserir ao banco
        print ("cliente adicionado ao banco!! nome:", nomeTemp," razao social: ",razaosoc," cnpj: ",cnpjTemp," data_inclusao: ",dataInclusao) #confirmação visual no backEnd
        db.session.add(cliente) #adiciona o cliente ao banco
        db.session.commit() #aplica a alteração no banco
        return jsonify(error=errorTemp,message="Cliente criado com sucesso",status=200) ,200  #Retorno ao front end
      else:
        return jsonify(error=errorTemp,message="Falha ao criar o cliente",status=statusTemp) , statusTemp  #Caso tenha dado algum erro retorna o erro através das variaveis salvas anteriormente
    except: 
      return jsonify(error="Informe nome, razao_social e cnpj", message="JSON vazio ou inexistente", status=400) , 400 #aqui é caso de algum erro diferente dos esperados retornar um Internal Error e o Runtime Error
  return createCliente  #retorno da blueprint