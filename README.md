# Leia com carinho!

Como resolvi o desafio ^^
=
Após muita pesquisa (referencias no final)...

Passo a passo feito para incialização do docker com PostgreSQL 

1- instalar win docker

2- instalar o kernel do linux wsl2 para pc x64

3- abrir CMD

1.CRIAÇÃO DO DOCKER
=

- docker pull postgres  			
- docker run --name PostgresDocker -e POSTGRES_PASSWORD=root -d -p 5432:5432 postgres:14.4-alpine
- docker ps 	 
- docker exec -it PostgresDocker bash 
- ls 							
- psql 						
- psql -U postgres	 	

agora estamos dentro do postgres com acesso a todos comandos e possibilidade para comandos SQL

- create database desafio;
- \l 	
- \c desafio
- \d

**FIM CRIAÇÃO DO DOCKER**


2.Codigos docker para verificar DB
-
- docker exec -it PostgresDocker(nomeImagem) bash
#executar imagem

- pwd
- psql -U postgres(nomeusuario) 		
#conectar no banco
- \l
#listar base de dados
-  create database nome; / drop database nome;
#criar e deletar db
- \c desafio(nomedatabase)
#conectar a base de dados
- \d
#listar relacionamentos

agora pode usar comandos SQL a vontade, usar **" ; "** no final

3.testando conexão ao docker pelo SQL SHELL (psql)
=
abrir o SQL SHELL (psql)
-------
**responder as perguntas de conexão:**
- Server: localhost
- Database: postgres
- Port: 5432
- Username: postgres
- Password: root

psql(14.4)
postgres=#

conseguimos conectar ao banco por fora do docker então está tudo ok

**Testando outros comandos**
-------
- \l  
#mostrou todos os bancos 
- \c desafio 
#conecta no banco desafio

you are now connected to database "desafio" as user "postgres".
desafio=#
- \d	
#mostrar relações

(did not find any relations)

conseguimos conectar ao nosso banco criado no docker de fora dele ja

-------------

4.Python
=

**Informações sobre o codigo em sí estão comentadas dentro do código**
-

**1 -** abrir terminal na pasta (no meu caso estou usando o ubuntu no windows)

**2 -** comandos para criar o enviroment

VENV
-
- python3 -m venv venv
 - source venv/bin/activate
 - pip install flask
 - pip install flask_sqlalchemy
 - pip install flask_migrate
 - pip install psycopg2-binary
 - source venv/bin/activate



--------------------------------
 - code .

agora estamos com nosso ambiente criado e estamos no code para poder começar a criar a parte python

**3 -**  apos setar as configs do banco e as migrações rodar o comando no terminal do code

Migration
-

- python
- from app import *
- db_create_all()
- exit()

----------

Verificar se deu certo a migration
-

**4 -** Conectar a base de dados no docker (desafio) e executar (select * from cliente; )  
sucesso, migrations foram subidas para o banco e a tabela ja possui codigo, nome, razaosocial, cnpj e data_inclusao

**5 -** para rodar o código (usei terminal ubuntu) 

**6 -** o docker foi usando o cmd mesmo

COMO RODAR O CÓDIGO
=

- Baixar repositorio

- SUBIR O DOCKER

- Na pasta do repositorio:

**abrir o terminal da pasta onde está os arquivos do codigo**

- CRIAR VENV

- source venv/bin/activate

**executar isto no terminal para subir as tabelas ao banco**
- python
- from app import *
- db.create_all()
- exit()

**ainda no terminal iniciar o sistema**
- flask run

------

**Prontinho agora tudo está rodando perfeitamente ^^**


ROTAS
=

**Todas rotas exceto GET estao tratadas para recusar envio sem JSON, JSON vazios ou com algum dado faltante**

**Nome e Razão Social estão em modo TITULO e são tratados para não possuir espaços duplos e nem começar ou terminar com espaço**

**CNPJ está configurado para aceitar apenas entradas com 14 dígitos**

**CNPJ e Razão Social estão configurados no back end para não aceitar serem inseridos repetidos tanto no POST quanto no PUT**

Criar novo Cliente:
-

**O "codigo" e a "data_cadastro" é auto gerado pelo sistema**

POST http://127.0.0.1:5000/createCli

	body raw JSON

		{ 
			 "nome":"novoNome",
			 "razao_social":"novaRazaoSocial",
			 "cnpj":"novoCNPJ" 
		}


Pegar lista de Clientes:
-

**Configurei para retornar uma lista JSON com todos os clientes e suas informações**

GET https://127.0.0.1:5000/listCli

Atualizar Cliente:
-

**Pode ser atualizado 1 apenas, 2 ou 3 dados ao mesmo tempo**

PUT http://127.0.0.1:5000/updateCli

	body raw JSON

		{
			"codigo":"numCodigo",
			"cnpj/nome/razao_social":"dado"
		}
	

		{
			"codigo":"8",
			"cnpj":"12345678901258",
			"nome":"Luis Guilherme",
			"razao_social":"DrZebra"
		}

Deletar Cliente:
-

DELETE http://127.0.0.1:5000/deleteCli

	body raw JSON

		{
			"codigo":"8"
		}

-------
Referencias:
=

- https://hub.docker.com/_/postgres
- https://docs.sqlalchemy.org/en/14/core/constraints.html
- https://docs.sqlalchemy.org/en/14/core/type_basics.html
- https://docs.sqlalchemy.org/en/14/orm/session_basics.html
- https://www.w3schools.com/python/python_strings.asp
- https://flask-sqlalchemy.palletsprojects.com/en/2.x/models/
- https://blog.geekhunter.com.br/flask-framework-python/
- https://www.digitalocean.com/community/tutorials/processing-incoming-request-data-in-flask-pt
- https://www.hostinger.com.br/tutoriais/o-que-e-http-error-e-principais-codigos-http
- https://www.prisma.io/dataguide/postgresql/5-ways-to-host-postgresql
- https://stackoverflow.com/questions/23717834/importerror-no-module-named-psycopg2-after-install
- https://stackoverflow.com/questions/37099564/docker-how-can-run-the-psql-command-in-the-postgres-container
- https://stackoverflow.com/questions/57130278/how-can-i-check-postgres-database-in-docker-volume
- https://stackoverflow.com/questions/47656071/commanderror-cant-locate-revision-identified-by-when-migrating-using-fla
- https://stackoverflow.com/questions/5022066/how-to-serialize-sqlalchemy-result-to-json
- https://stackoverflow.com/questions/20808672/how-to-get-a-list-from-query-in-sqlalchemy
- https://stackoverflow.com/questions/7824101/return-http-status-code-201-in-flask
- https://www.geeksforgeeks.org/python-convert-json-to-string/
- https://www.youtube.com/watch?v=levz4eumJ98&ab_channel=PedroImpulcetto
- https://www.youtube.com/watch?v=uNmWxvvyBGU&ab_channel=PrettyPrinted
- https://www.youtube.com/watch?v=ca-Vj6kwK7M&ab_channel=Codemy.com
- https://www.youtube.com/watch?v=Ad-inC3mJfU&ab_channel=k0nzebuilds
- https://www.youtube.com/watch?v=aHbE3pTyG-Q&ab_channel=Amigoscode
- https://www.youtube.com/watch?v=Nm1FPcsPnWg&list=PLXmMXHVSvS-BlLA5beNJojJLlpE0PJgCW&index=29&ab_channel=PrettyPrinted
https://www.youtube.com/watch?v=29OTNdCIrNU&list=PLXmMXHVSvS-BlLA5beNJojJLlpE0PJgCW&index=22&ab_channel=PrettyPrinted
- https://www.delftstack.com/pt/howto/python/python-check-if-character-is-number/#:~:text=na%20declara%C3%A7%C3%A3o%20condicional.-,Use%20o%20m%C3%A9todo%20isdigit()%20para%20verificar%20se%20um%20determinado,todos%20os%20caracteres%20forem%20d%C3%ADgitos.

