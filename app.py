from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from env import API_URI
from routes.createCli import createClientBlueprint
from routes.listCli import listClientBlueprint

app = Flask(__name__) #inicializar app

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False   #não ficar dando notificação a cada alteração
app.config['SQLALCHEMY_DATABASE_URI'] = API_URI #API_URI seria para poder esconder com o .gitIgnore (aqui vai as senhas url...)

db = SQLAlchemy(app)   #inicialização do banco
db.create_all()    

class Cliente(db.Model): #tabaela
    codigo = db.Column(db.Integer, primary_key=True) # coluna
    nome = db.Column(db.String(120), nullable=False) # coluna
    razao_social = db.Column(db.String(255), nullable=False) # coluna
    cnpj = db.Column(db.String(18), nullable=False) # coluna #aqui coloquei o tamanho como 18 não 14 caso queira salvar 00.000.000/0001-12 em vez de apenas 00000000000112
    data_inclusao = db.Column(db.DateTime, nullable=False) # coluna

    def __repr__(self): #retorno para quando chama a info da tabela
        retorno = {"Codigo":{self.codigo}, "Nome":{self.nome}, "razao_social":{self.razao_social}, "cnpj":{self.cnpj}, "data_inclusao":{self.data_inclusao}}
        return retorno  #aqui estou retornando o cliente inteiro como JSON (no caso do python dicionario)

app.register_blueprint(createClientBlueprint(db, Cliente))  #registrando a rota /post do cliente (create)
app.register_blueprint(listClientBlueprint(db,Cliente)) #registrando a rota /get do cliente (lista)