#%%
from flask import Flask
from config import Config #Se refere ao arquivo config.py classe Config
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
print('__name__',__name__)


app.config['SECRET_KEY'] = '4q3r59p8yhglkjh43598ys7dgkjhq43509876sertgASDA$@#iuy'

#%% Configuracoes de conxao com o database
app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc://sa:123456@localhost\SQLEXPRESS2019/ppablos?driver=ODBC+Driver+17+for+SQL+Server'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
db = SQLAlchemy(app)

from application import routes #arquivo routes.py dentro da pasta application

