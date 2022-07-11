from datetime import datetime
from flask import Blueprint, Response, request, jsonify
from sqlalchemy import delete

#primeiro vez criando algo do tipo em python então vamos lá ^^

def deleteClientBlueprint(db, Cliente): #funcao para fazer a criação da rota por fora do app.py
  
  deleteCliente = Blueprint('deleteCliente', __name__)  #criação do nome da blueprint
  @deleteCliente.route('/deleteCli', methods=['DELETE']) #criação da rota 
  def delete_cliente(): #funcionamento da rota
    
    statusTemp = 0 #setando status para retorno
    errorTemp = "null" #setando erro para retorno
    
    try:

      request_data = request.get_json(force=True) #aqui pega o JSON do postman ou do front end...

      if not request_data: #verifica se possui JSON
        statusTemp=400
        errorTemp="Informe JSON com o codigo do cliente"
      else:

        if not 'codigo' in request_data: #verificando se possui codigo no JSON
          statusTemp=400
          errorTemp="Informe um codigo no JSON"
        else:
         
          codigoTemp = request_data['codigo']
         
          if not codigoTemp:
            statusTemp=400
            errorTemp="Informe um codigo válido"
          else:
            
            if not (codigoTemp.isdigit()):
              statusTemp=400
              errorTemp="codigo deve ser digito"
            else:

              cli = Cliente.query.filter_by(codigo = codigoTemp).first()

              if not cli:
                statusTemp=400
                errorTemp="Cliente não encontrado"
              else:

                stmt = delete(Cliente).where(Cliente.codigo == cli.codigo).execution_options(synchronize_session="fetch")
                db.session.execute(stmt) #adiciona o cliente ao banco
                db.session.commit() #aplica a alteração no banco
                return jsonify(error=errorTemp,message="Cliente deletado com sucesso",status=200), 200  #Retorno ao front end
      return jsonify(error=errorTemp, message="Erro ao deletar", status=statusTemp), statusTemp #retorno ao front end...
    except:
      return jsonify(error="JSON ausente ou incompleto", message="Falha ao receber o pedido", status=400), 400 #aqui é caso de algum erro diferente dos esperados retornar um Internal Error e o Runtime Error
  return deleteCliente  #retorno da blueprint