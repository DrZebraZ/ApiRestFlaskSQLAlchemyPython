from datetime import datetime
from flask import Blueprint, Response, request, jsonify

from verifyStr import DeleteDoubleSpaces, VerifyEmptyStr

#primeiro vez criando algo do tipo em python então vamos lá ^^

def createClientBlueprint(db, Cliente): #funcao para fazer a criação da rota por fora do app.py
  
  createCliente = Blueprint('createCliente', __name__)  #criação do nome da blueprint
  @createCliente.route('/createCli', methods=['POST']) #criação da rota 
  def create_cliente(): #funcionamento da rota
    
    statusTemp = 0 #setando status para retorno
    errorTemp = "null" #setando erro para retorno

    try:

      request_data = request.get_json(force=True) #aqui pega o JSON do postman ou do front end...
      
      if not request_data:
        statusTemp=400
        errorTemp="JSON vazio, informe: nome, razao_social e cnpj"
      else:

        if not ('nome' in request_data and 'razao_social' in request_data and 'cnpj' in request_data):
          statusTemp=400
          errorTemp="Informe nome, razao_social e cnpj"
        else:

          nomeTemp = DeleteDoubleSpaces(request_data['nome']).title() #seta nome para testes
          razaosoc = DeleteDoubleSpaces(request_data['razao_social']).title() #seta razaosocial para testes
          cnpjTemp = request_data['cnpj'] #seta cnpj para testes
          
          #limpando nome para validação
          if VerifyEmptyStr(nomeTemp):
            statusTemp=400
            errorTemp="informe um nome válido"
          else:

            #limpando razao social para validação
            if VerifyEmptyStr(razaosoc):
              statusTemp=400
              errorTemp="informe uma razao_social válida"
            else:         #caso razao social não seja nula verifica se não possui nenhuma igual no banco
              teste = Cliente.query.filter_by(razao_social=razaosoc).first()
              if (teste):     #se possuir alguma ja no banco retorna que ja está em uso
                statusTemp = 400
                errorTemp = "Razão social já em uso"
              else:

                #verificando CNPJ
                if (not cnpjTemp or len(cnpjTemp)!=14 or not cnpjTemp.isdigit()): #se CNPJ estiver vazio, for diferente de 14 da erro
                  statusTemp = 400
                  errorTemp = "CNPJ deve conter 14 digitos"
                else: #caso passe no if anterior se estiver no banco ja da erro também
                  teste = Cliente.query.filter_by(cnpj=cnpjTemp).first()
                  if (teste):
                    statusTemp = 400
                    errorTemp = "CNPJ já em uso"  # erro ^^
                  else:

                      #se em nenhum momento deu erro durante a verificação passa para salvar no banco
                      dataInclusao = datetime.now()  #como é data de inclusão entao ele pega a data da hora de inclusao para jogar no banco
                      cliente = Cliente(nome=nomeTemp, razao_social=razaosoc, cnpj=cnpjTemp, data_inclusao=dataInclusao)  #cria o cliente para inserir ao banco
                      print ("cliente adicionado ao banco!! nome:", nomeTemp," razao social: ",razaosoc," cnpj: ",cnpjTemp," data_inclusao: ",dataInclusao) #confirmação visual no backEnd
                      db.session.add(cliente) #adiciona o cliente ao banco
                      db.session.commit() #aplica a alteração no banco
                      return jsonify(error=errorTemp,message="Cliente criado com sucesso",status=200) ,200  #Retorno ao front end
                      #Caso tenha dado algum erro retorna o erro através das variaveis salvas anteriormente
      #return do try
      return jsonify(error=errorTemp,message="Erro ao criar cliente",status=statusTemp) , statusTemp
    except: 
      return jsonify(error="JSON ausente ou incompleto", message="Falha ao receber o pedido", status=400), 400  #aqui é caso de algum erro diferente dos esperados retornar um Internal Error e o Runtime Error
  return createCliente  #retorno da blueprint