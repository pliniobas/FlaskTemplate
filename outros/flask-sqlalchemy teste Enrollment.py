#%%
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc://sa:123456@localhost\SQLEXPRESS2019/ppablos?driver=ODBC+Driver+17+for+SQL+Server'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Enrollment(db.Model):
    courseID    =   db.Column (db.Integer, primary_key = True)
    user_id     =   db.Column (db.Integer, nullable = False)

class Courses(db.Model):
    courseID    =   db.Column (db.Integer, primary_key = True)
    title       =   db.Column (db.String(80), nullable = False, unique=True )
    description =   db.Column (db.String(255), nullable = True)
    credits     =   db.Column (db.Integer, nullable = False)
    term        =   db.Column (db.String)
#%%

temp = Enrollment.query.filter_by(user_id = 1).all()
temp = [aux.courseID for aux in temp]
print(temp)

#%%
classes = Courses.query.filter(Courses.courseID.in_(temp)).all()
# classes = [aux.__dict__ for aux in classes]
print(classes)

#%%
classes = Courses.query.filter(Courses.courseID.in_([1,2])).all()
print(classes)


#%%

type(classes[0])

# %%
for aux in classes:
    print("###########################################")
    print(aux.courseID)
    print(aux.title)
    print(aux.description)
    print(aux.credits)
    print(aux.term)  
# %%
dict(classes)
# %%
type(classes)
# %%
type(classes[0])
# %%
dict(classes[0])
# %%
dir(classes[0])
# %%
classes[0].__dict__
# %%
classes[0].term
# %%
