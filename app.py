from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from env import API_URI
from routes.createCli import createClientBlueprint
from routes.deleteCli import deleteClientBlueprint
from routes.listCli import listClientBlueprint
from routes.updateCli import updateClientBlueprint

app = Flask(__name__) #inicializar app

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False   #não ficar dando notificação a cada alteração
app.config['SQLALCHEMY_DATABASE_URI'] = API_URI #API_URI seria para poder esconder com o .gitIgnore (aqui vai as senhas url...)

db = SQLAlchemy(app)   #inicialização do banco
db.create_all()    

class Cliente(db.Model): #tabaela

    codigo = db.Column(db.Integer, primary_key=True) # coluna
    nome = db.Column(db.String(120), nullable=False) # coluna
    razao_social = db.Column(db.String(255), nullable=False) # coluna
    cnpj = db.Column(db.String(14), nullable=False) # coluna #aqui coloquei o tamanho como 14 salva apenas 00000000000112 sem os - - - / .
    data_inclusao = db.Column(db.DateTime, nullable=False) # coluna

    def __repr__(self): #retorno para quando chama a info da tabela
        retorno = {"codigo":{self.codigo}, "nome":{self.nome}, "razao_social":{self.razao_social}, "cnpj":{self.cnpj}, "data_inclusao":{self.data_inclusao}}
        return retorno  #aqui estou retornando o cliente inteiro como JSON (no caso do python dicionario)

app.register_blueprint(createClientBlueprint(db, Cliente))  #registrando a rota post do cliente (create)
app.register_blueprint(listClientBlueprint(db,Cliente)) #registrando a rota get do cliente (lista)
app.register_blueprint(updateClientBlueprint(db,Cliente)) #registrando a rota put do cliente (update)
app.register_blueprint(deleteClientBlueprint(db,Cliente)) #registrando a rota delete do cliente (delete)