#%%
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  8 10:03:15 2021

@author: plinio silva
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc://sa:123456@localhost\SQLEXPRESS2019/ppablos?driver=ODBC+Driver+17+for+SQL+Server'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

#%%

#Cria o modelo da tabela, para criacao ou para consulta
class Users(db.Model): 
    user_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String( ), nullable=False)
    admin = db.Column(db.Boolean, nullable = True)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def get_password(self, password):
        return check_password_hash(self.password, password)


# Checa se a table já existe, se nao existir, cria uma nova.
if 'users' not in db.engine.table_names():
    db.create_all() #Cria a nova tabela


#modelo de usuario para tentar criar no dataframe
usuario = Users(first_name="Plinio",last_name="Silva",email = "pliniobas@gmail.com",
                password = "123456",admin = False)

#%%
# Checa nome de usuarios na tabela
bool_usuario_registrado = False
users = Users.query.all()
for user in users:
    if user.email == usuario.email:
        bool_usuario_registrado = True
        print('encontrado usuario já registrado')

#ou entao, usa o proprio SQL para procurar pelo usuario... mais inteligente do que acima
user = Users.query.filter_by(email = usuario.email).first() #Essa query do SQL retorna o usuario filtrado por email
if user: #and  user.get_password(password) == password: #user é None se nao for encontrado, então é False.
    print('encontrado usuario já registrado')
else:
    print('Usuario ainda nao registrado')

#%% Registra o usuario no database caso ele ainda nao exista
if not bool_usuario_registrado:
    db.session.add(usuario)
    db.session.commit()

    users = Users.query.all()
    for user in users:
        if user.email == usuario.email:


            
#%%

user = Users.query.filter_by(email = 'pliniobas2@gmail.com').first()
user.password

#%%

a= Users.query.count() #retorna o numero do id
dir(a)
