# Importa o FastAPI
from fastapi import FastAPI
from fastapi.responses import JSONResponse
# Importa o SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String
#  Importa o os
import os


# Instancia o FastAPI
app = FastAPI()

SQLALCHEMY_DATABASE_URL = os.environ.get('DATABASE_URL')

engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Cria uma sessão para o banco de dados
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = SessionLocal()

# Cria uma classe que herda do declarative_base
Base = declarative_base()

# Cria uma classe User que herda da classe Base
class User(Base):
	# Define o nome da tabela
	__tablename__ = "users"
	# Define o id como uma coluna do tipo Integer
	id = Column(Integer, primary_key=True, index=True)
	# Define o nome como uma coluna do tipo String
	name = Column(String)
	# Define o email como uma coluna do tipo String
	email = Column(String)

# Cria as tabelas no banco de dados
Base.metadata.create_all(bind=engine)

# Cria uma rota de GET com o path "/"
@app.get("/")
def read_root():
	# Retorna um JSON simples com Hello World
	return {"Hello": "World"}

# Cria uma rota de GET com o path "/users"
@app.get("/users")
def read_users():
	# Cria uma variável users que recebe todos os usuários
	users = session.query(User).all()
	# Cria uma lista vazia
	users_list = []
	# Para cada usuário em users
	for user in users:
		# Cria um dicionário com o id, nome e email do usuário
		user_dict = {"id": user.id, "name": user.name, "email": user.email}
		# Adiciona o dicionário na lista
		users_list.append(user_dict)
	# Retorna um JSON com a lista de usuários
	return JSONResponse(content=users_list)

# Cria uma rota de GET com o path "/users/{user_id}"
@app.get("/users/{user_id}")
def read_user(user_id: int):
	# Cria uma variável user que recebe o usuário com o id fornecido
	user = session.query(User).filter(User.id == user_id).first()
	# Cria um dicionário com o id, nome e email do usuário
	user_dict = {"id": user.id, "name": user.name, "email": user.email}
	# Retorna um JSON com o usuário
	return JSONResponse(content=user_dict)

# Cria uma rota de POST com o path "/users"
@app.post("/users")
def create_user(name: str, email: str):
	# Cria um objeto da classe User
	user = User(name=name, email=email)
	# Adiciona o usuário ao banco de dados
	session.add(user)
	# Salva as alterações no banco de dados
	session.commit()
	# Retorna um JSON com o id, nome e email do usuário
	return JSONResponse(content={"id": user.id, "name": user.name, "email": user.email})

# Cria uma rota de PUT com o path "/users/{user_id}"
@app.put("/users/{user_id}")
def update_user(user_id: int, name: str, email: str):
	# Cria uma variável user que recebe o usuário com o id fornecido
	user = session.query(User).filter(User.id == user_id).first()
	# Atualiza o nome do usuário
	user.name = name
	# Atualiza o email do usuário
	user.email = email
	# Salva as alterações no banco de dados
	session.commit()
	# Retorna um JSON com o id, nome e email do usuário
	return JSONResponse(content={"id": user.id, "name": user.name, "email": user.email})

# Cria uma rota de DELETE com o path "/users/{user_id}"
@app.delete("/users/{user_id}")
def delete_user(user_id: int):
	# Cria uma variável user que recebe o usuário com o id fornecido
	user = session.query(User).filter(User.id == user_id).first()
	# Remove o usuário do banco de dados
	session.delete(user)
	# Salva as alterações no banco de dados
	session.commit()
	# Retorna um JSON com o id, nome e email do usuário
	return JSONResponse(content={"id": user.id, "name": user.name, "email": user.email})