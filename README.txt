DESAFIO:

1. Criar / rodar um docker com o PostgreSQL14
	a. https://hub.docker.com/_/postgres
2. Utilizando Python 3.6+ e o microframework FLASK:
	a. Crie uma API REST utilizando JSON para realizar um CRUD completo em uma tabela CLIENTE
		i. GET (Lista clientes)
		ii. POST (Criar cliente)	
		iii. PUT (Editar cliente)
		iv. DELETE (Remover cliente)	
	b. Dê preferência para o modelo de Blueprints do Flask.
	c. Se possível, utilizar algum ORM para conexão e manutenção das querys
		(Sugestão: SQL Alchemy)
	d. Criar Migrações para criação da tabela no banco com os campos:
		i. código (primary_key / not null) ,
		ii. nome (not null)
		iii. razão social (not null)
		iv. cnpj (not null),
		v. data_inclusao (datetime / not null)
	e. Criar um Padrão de Respostas para API, com status_code e mensagens de sucesso ou erro, como por exemplo.
	{
		"status": 200,
		"message": "Cliente criado com sucesso"
		"error": "null"
	}

Como resolvi o desafio ^^

Após muita pesquisa (referencias no final)...

Passo a passo feito para incialização do docker com PostgreSQL 14.4

1- instalar win docker
2- instalar o kernel do linux wsl2 para pc x64
3- abrir CMD

=================================== CRIAÇÃO DO DOCKER ===================================

 - docker pull postgres  //baixar as bibliotecas/dependencias postgreSQL
 - docker run --name PostgresDocker -e POSTGRES_PASSWORD=root -d -p 5432:5432 postgres:14.4-alpine   //criar imagem do postgree na versão 14.4-alpine (mais leve)
 - docker ps 	 //para ver os conteiners
 - docker exec -it PostgresDocker bash 	//executar a imagem criada
 - pwd 	//ir para pasta
 - ls 	//ver a estrutura
 - psql 	//deu erro por falta da permissao ao root (admin)
 - psql -U postgres	 // chamar o PSQL com o username "postgres"

 //agora estamos dentro do postgres com acesso a todos comandos
 //e possibilidade para comandos SQL (create database, tables...)

 - \l 	//comando para listar os schemas
 - create database desafio; 	//criando o banco desafio (por os ; pra n dar erro)
 - \l 	//agora podemos ver o banco ja criado
 - \c desafio  	//conectar ao banco "desafio" como o usuario "postgres"
 - \d 	//did not find any relations (ainda não possui nada no banco)

=================================== CRIAÇÃO DO DOCKER ===================================

//Até aqui criamos o banco dentro de um docker agora vamos conectar nele de fora do docker para testar se deu tudo certo

//Codigos docker para verificar DB
// docker exec -it nomeImagem bash (executar imagem)
// pwd
// psql -U postgres(nomeusuario) (conectar no banco)
// \l (listar base de dados)
// create database nome / drop database nome (criar e deletar db)
// \c nomedatabase (conectar a base de dados)
// \d listar relacionamentos
// apos entrar na base de dados (\c nome) pode usar comandos SQL a vontade lembrando de usar ";" no final
 
4- instalação do PosgreSQL 14.4.1 x64
5- testando conexão ao docker pelo SQL SHELL (psql)
6- Pesquisa windows (SQL SHELL) e abrir o SQL SHELL (psql)
//responder as perguntas de conexão:
 - Server: localhost
 - Database: postgres
 - Port: 5432
 - Username: postgres
 - Password: root
// psql(14.4)
// postgres=#
// conseguimos conectar ao banco por fora do docker então está tudo ok
// testando outros comandos
 - \l (mostrou todos os bancos) 
 - \c desafio
//you are now connected to database "desafio" as user "postgres".
//desafio=#
 - \d
//did not find any relations
(conseguimos conectar ao nosso banco criado no docker de fora dele ja)

agora começar parte de Python

1 criar pasta
2 abrir terminal na pasta (no meu caso estou usando o ubuntu no windows)
3 comandos

======================================== VENV ========================================

 - python3 -m venv venv //criar ambiente
 - source venv/bin/activate
 - pip install flask flask_sqlal
 - pip install flask_sqlalchemy
 - pip install flask_migrate
 - pip install psycopg2-binary //foi necessário instalar durante a criação do projeto também
 - source venv/bin/activate

======================================================================================

 - code .

//agora estamos com nosso ambiente criado 
//e estamos no code para poder começar a criar a parte python

4 apos setar as configs do banco e as migrações rodar o comando no terminal do code
 - python
 - from app import *
 - db_create_all()
 - exit()
 //migração da base de dados
5 conectar a base de dados no docker (desafio) e executar (select * from cliente;) //verificar se deu certo o codigo
// sucesso, migrations foram subidas para o banco e a tabela ja possui codigo, nome, razaosocial, cnpj e data_inclusao

Toda info do por que utilizei cada coisa no programa está no código em si

6 para rodar o código (terminal ubuntu)  <--------- após ter feito a criação do docker

 - source venv/bin/activate

//---executar isso apenas se necessitar subir as tabelas ao banco ----
 - python
 - from app import *
 - db.create_all()
 - exit
//--------------------------------------------------------------------
 
- flask run  //iniciar banco

para usar as rotas o padrão é:

Criar novo Cliente:
POST http://127.0.0.1:5000/createCli
body raw JSON
{ 
  "nome":"novoNome",
  "razao_social":"novaRazaoSocial",
  "cnpj":"novoCNPJ" 
}

//o codigo é auto gerado pelo sistema e a data de cadastro também

Pegar lista de Clientes:
GET https://127.0.0.1:5000/listCli

Referencias:
Links utilizados para pesquisa:

https://hub.docker.com/_/postgres
https://docs.sqlalchemy.org/en/14/core/constraints.html
https://docs.sqlalchemy.org/en/14/core/type_basics.html
https://flask-sqlalchemy.palletsprojects.com/en/2.x/models/
https://blog.geekhunter.com.br/flask-framework-python/
https://www.digitalocean.com/community/tutorials/processing-incoming-request-data-in-flask-pt
https://www.hostinger.com.br/tutoriais/o-que-e-http-error-e-principais-codigos-http
https://www.prisma.io/dataguide/postgresql/5-ways-to-host-postgresql
https://stackoverflow.com/questions/23717834/importerror-no-module-named-psycopg2-after-install
https://stackoverflow.com/questions/37099564/docker-how-can-run-the-psql-command-in-the-postgres-container
https://stackoverflow.com/questions/57130278/how-can-i-check-postgres-database-in-docker-volume
https://stackoverflow.com/questions/47656071/commanderror-cant-locate-revision-identified-by-when-migrating-using-fla
https://stackoverflow.com/questions/5022066/how-to-serialize-sqlalchemy-result-to-json
https://stackoverflow.com/questions/20808672/how-to-get-a-list-from-query-in-sqlalchemy
https://stackoverflow.com/questions/7824101/return-http-status-code-201-in-flask
https://www.geeksforgeeks.org/python-convert-json-to-string/
https://www.youtube.com/watch?v=levz4eumJ98&ab_channel=PedroImpulcetto
https://www.youtube.com/watch?v=uNmWxvvyBGU&ab_channel=PrettyPrinted
https://www.youtube.com/watch?v=ca-Vj6kwK7M&ab_channel=Codemy.com
https://www.youtube.com/watch?v=Ad-inC3mJfU&ab_channel=k0nzebuilds
https://www.youtube.com/watch?v=aHbE3pTyG-Q&ab_channel=Amigoscode
https://www.youtube.com/watch?v=Nm1FPcsPnWg&list=PLXmMXHVSvS-BlLA5beNJojJLlpE0PJgCW&index=29&ab_channel=PrettyPrinted
https://www.youtube.com/watch?v=29OTNdCIrNU&list=PLXmMXHVSvS-BlLA5beNJojJLlpE0PJgCW&index=22&ab_channel=PrettyPrinted