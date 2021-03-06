from datetime import datetime
from flask import Blueprint, request, jsonify

def listClientBlueprint(db, Cliente):   #não necessita retorno (criei para poder fazer as rotas por fora do APP.py)
  listCliente = Blueprint('listCliente', __name__)   #setando a blueprint
  @listCliente.route('/listCli', methods=['GET'])   #setando a rota
  def list_cliente():       #funcionamento da rota

    clijson={}    #setando o dicionario (json)
    clientes = db.engine.execute('select * from Cliente')  #query

    for cli in clientes: 
      #para cada cliente na query dos clientes criar uma nova posição no JSON com o valor da posição o codigo do cliente
      #dentro da posição (codigo) um novo JSON com as outras informações do cliente
      clijson[cli.codigo] = {"nome":cli.nome,"razao_social":cli.razao_social,"cnpj":cli.cnpj,"data_inclusao":cli.data_inclusao}

    if clijson=={}:
      return jsonify(erro="null",message="Lista vazia", status=200),200  

    return jsonify(error="null",message=clijson,status=200),200 #retorno da rota
    
  return listCliente #retorno do blueprint