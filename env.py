
#Ambiente para setar as variáveis sensiveis 
#criado normalmente para colocar no gitIgnore e não ir ao github com infos pessoais
API_USER='postgres'   #usuario
API_PASSWORD='root'   #senha
API_HOST='localhost'     #link
API_DATABASE='desafio'    #schema
API_URI=("postgresql://"+API_USER+":"+API_PASSWORD+"@"+API_HOST+"/"+API_DATABASE)   #api_uri de retorno para o SQLAlchemy
