from multiprocessing import synchronize
from flask import Blueprint, Response, request, jsonify
from sqlalchemy import update

from verifyStr import DeleteDoubleSpaces, VerifyEmptyStr

def updateClientBlueprint(db, Cliente):  #retorna blueprint
  updateCliente = Blueprint('updateCliente', __name__)   #seta bluerpint
  @updateCliente.route('/updateCli', methods=['PUT'])  
  def list_cliente():     

    statusTemp=0
    errorTemp=""

    try: 

      request_data = request.get_json(force=True)

      if not request_data:  #se n tiver json retornar erro
        statusTemp=400
        errorTemp="Informe no JSON codigo do cliente e dados a serem atualizados"
      else: #erro caso nao possua nenhuma informação no JSON

        if not 'codigo' in request_data:  #procurar cliente  
          statusTemp = 400
          errorTemp = "Informe o codigo do cliente"       
        else: #erro caso nao possua codigo no JSON
        
          codigoTemp = request_data['codigo']

          if not codigoTemp:
            statusTemp=400
            errorTemp="Informe um codigo válido"
          else:
            
            cli = Cliente.query.filter_by(codigo = codigoTemp).first()  #busca cliente
            
            if not cli: #caso exista cliente
              statusTemp=400
              errorTemp = "Informe um codigo existente"
            else: #erro caso o codigo nao possua no banco
              
              if not ('nome' in request_data or 'razao_social' in request_data or 'cnpj' in request_data): #caso exista algum dado a ser atualizado
                statusTemp=400
                errorTemp="Informe nome, razao_social ou cnpj para alterar"
              else: #erro caso nao seja informado nada para atualizar
                
                if 'nome' in request_data:

                  nomeTemp = DeleteDoubleSpaces(request_data['nome']).title()
                  
                  if VerifyEmptyStr(nomeTemp):
                    statusTemp=400
                    errorTemp="informe um nome válido"
                  else:  #se o nome não for nulo  
                    cli.nome = nomeTemp

                if 'razao_social' in request_data:
                  
                  razaosoc = DeleteDoubleSpaces(request_data['razao_social']).title()
                
                  if VerifyEmptyStr(razaosoc):
                    statusTemp=400
                    errorTemp="informe uma razao_social válida"
                  else:
                    if (razaosoc != cli.razao_social):  #se for diferente (atualizada)
                      teste = Cliente.query.filter_by(razao_social=razaosoc).first()
                      if teste: #se ja possuir essa razao social dar erro
                        statusTemp=400
                        errorTemp="Razão social ja em uso"
                      else: #se nao possuir no banco salvar a nova
                        cli.razao_social = razaosoc

                if 'cnpj' in request_data:  
                  
                  cnpjTemp = request_data['cnpj']
                  
                  if (not cnpjTemp or len(cnpjTemp)!=14 or not cnpjTemp.isdigit()):
                    statusTemp=400
                    errorTemp="Informe um cnpj de 14 digitos"
                  else:
                    if (cnpjTemp != cli.cnpj):  #se for diferente (atualizado)
                      teste = Cliente.query.filter_by(cnpj=cnpjTemp).first()
                      if teste: #erro caso ja possua o novo
                        statusTemp=400
                        errorTemp="CNPJ ja em uso"
                      else: #salva caso o novo não exista no banco
                        cli.cnpj = cnpjTemp

                if (statusTemp == 0):  #se nao possuiu nenhum erro enviar ao banco
                  #aqui esta enviando com os proprios valores e os atualizados
                  stmt = update(Cliente).where(Cliente.codigo == cli.codigo).values(nome=cli.nome, razao_social=cli.razao_social, cnpj=cli.cnpj).execution_options(synchronize_session ="fetch")
                  db.session.execute(stmt)
                  db.session.commit()
                  return jsonify(error="null", message="Atualizado com sucesso", status=200), 200  #retorno da atualização 
      #retorno do Try
      return jsonify(error=errorTemp,message="Erro ao atualizar",status=statusTemp), statusTemp #retorno caso possua algum erro
    except: #erro caso não possua JSON
      return jsonify(error="JSON ausente ou incompleto", message="Falha ao receber o pedido", status=400), 400 
  return updateCliente #retorno do blueprint