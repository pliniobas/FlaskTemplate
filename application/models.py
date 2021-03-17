import flask
from application import db
from werkzeug.security import generate_password_hash, check_password_hash

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


class Courses(db.Model):
    courseID    =   db.Column (db.Integer, primary_key = True)
    title       =   db.Column (db.String(80), nullable = False, unique=True )
    description =   db.Column (db.String(255), nullable = True)
    credits     =   db.Column (db.Integer, nullable = False)
    term        =   db.Column (db.String)

class Enrollment(db.Model):
    courseID    =   db.Column (db.Integer, primary_key = True)
    user_id     =   db.Column (db.Integer, nullable = False)
    



# Abaixo seria com o MongoDB
# import flask
# from application import db
# from werkzeug.security import generate_password_hash, check_password_hash

# class User(db.Document):
#     user_id     =   db.IntField( unique=True )
#     first_name  =   db.StringField( max_length=50 )
#     last_name   =   db.StringField( max_length=50 )
#     email       =   db.StringField( max_length=30, unique=True )
#     password    =   db.StringField( )

#     def set_password(self, password):
#         self.password = generate_password_hash(password)

#     def get_password(self, password):
#         return check_password_hash(self.password, password)    

# class Course(db.Document):
#     course_id   =   db.StringField( max_length=10, unique=True )
#     title       =   db.StringField( max_length=100 )
#     description =   db.StringField( max_length=255 )
#     credits     =   db.IntField()
#     term        =   db.StringField( max_length=25 )

# class Enrollment(db.Document):
#     user_id     =   db.IntField()
#     course_id   =   db.StringField( max_length=10 )