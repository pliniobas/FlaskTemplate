from application import app #variavel app, dentro da pasta application/__init__.py
from application import db #variavel db, dentro da pasta application/__init__.py
from application.forms import LoginForm, RegisterForm 
from application.models import Users, Courses, Enrollment
from flask import render_template, request, json, Response,redirect,flash,url_for,session
import os
from os.path import join

#%%

#Cria o modelo da tabela para criacao ou para consulta no database
#A conexao ao database eh feita no arquivo __init__.py

folder_programa = os.getcwd()
pasta_pablos = join(folder_programa,'../../../FTP/pmpas/perfilador')

@app.route("/")
@app.route("/index")
@app.route("/home")
def index():
    dic = dict(folder_programa = folder_programa,
        pasta_pablos = pasta_pablos
        )

    return render_template("index.html", indexhl = True , logedin = True, dic = dic)

@app.route("/courses")
@app.route("/courses/<term>")
def courses( term = None):
    if term is None:
        term = "Spring - saude"
    classes = Courses.query.all()

    return render_template("courses.html",courseData = classes, courseshl = True, term = term)

@app.route("/enrollment" , methods = ["GET","POST"])
def enrollment():

    if not session.get('username'):
        return redirect(url_for('index'))

    if 'enrollment' not in db.engine.table_names():
        db.create_all() #Cria a nova tabela
        flash("A tabela enrollment nao foi encontrada e uma nova tabela foi gerada","danger")

    courseID = request.form.get('courseID')
    if courseID:
        courseID = int(courseID) #cast para int caso exista porque na databank esta como inteiro

    courseTitle = request.form.get('title')
    user_id = session.get("user_id")
   
    #procura por cursos que o usuario ja esteja inscrito
    courseIDlist = []
    for aux in Enrollment.query.filter_by(user_id = user_id).all():
        courseIDlist.append(aux.courseID)


    if courseID: #courseID será None caso não venha um form... resultado da funcao request.form.get('courseID')  
        if courseID in session["courseIDlist"]:
            flash(f" Opa, já registrado","danger")  
            return redirect(url_for("courses"))

        else:
            enroll = Enrollment()
            enroll.courseID = courseID
            enroll.user_id = user_id
            
            db.session.add(enroll)
            db.session.commit()
            flash(f"Você foi inscrito com sucesso em {courseTitle}!","success")

    
    #procura novamente por cursos que o usuario ja esteja inscrito porque pode ter feito alguma nova inscricao
    #no form anterior
    session['courseIDlist'] = []
    for aux in Enrollment.query.filter_by(user_id = user_id).all():
        session['courseIDlist'].append(aux.courseID)


    #procura pelo atributos dos cursos ao qual o usuario se inscreveu:
    temp = [aux for aux in session['courseIDlist']]
    classes = Courses.query.filter(Courses.courseID.in_(temp)).all() #string meio enrolada... tirei o stackoverflow
    
    #o objeto retornado na lista classes nao pode ser passado diretamente para o template Jinja, da erro.
    # eh retirado o dictionary desses  
    classes = [aux.__dict__ for aux in classes]
  

    title = 'Enrollment'
    return render_template("enrollment.html", enrollmenthl=True, classes = classes, title = title)    

@app.route("/pag1")
def pag1():
    dic = dict(
        exemplo1 = "Dados a serem passados para o template",
        exemplo2 = "O melhor é passar um dictionary, pois varias variaveis podem ser passada dentro de uma só",
        exemplo3 = ["Inclusive","pode","ser","passado","funções como type e list!"]
    )
    return render_template("pag1.html",dic = dic, type = type,list = list, pag1hl = True )

@app.route("/pag2")
def pag2():
    return render_template("pag2.html", pag2hl = True )

@app.route("/login", methods=["GET","POST"])
def login():
    if session.get('username'):
        return redirect(url_for('index'))

    form = LoginForm()
        
    if form.validate_on_submit() == True:
        email        = form.email.data #esse é o email submetido pelo usuario
        password     = form.password.data #esse é o password submetido pelo usuario
        
        user = Users.query.filter_by(email = email).first() #Essa query do SQL retorna o usuario filtrado por email
        
        if user and  user.get_password(password): #user é None se nao for encontrado, então é False.
            flash(f"{user.first_name}, You are successufully logged in", "success")
            session["user_id"] = user.user_id
            session["username"] = user.first_name
            return redirect("/index")
        else:
            flash("Something went wrong. Try again","danger")
            

    return render_template("login.html" , loginhl = True, form = form, title = "Login" )
    # return render_template("login.html", title="Login", form=form, login=True )

@app.route('/logout')
def logout():

    if not session.get('username'):
        return redirect(url_for('index'))

    session["user_id"] = False
    session.pop('username',None)
    return redirect(url_for('index'))


@app.route("/register",methods = ["GET","POST"])
def register():
    
    if session.get('username'):
        return redirect(url_for('index'))

    form = RegisterForm()
    print('######################################## 0')
    #Checa se a tabela de usuarios existe, e cria caso nao exista.
    if 'users' not in db.engine.table_names():
        print('######################################## 2')
        db.create_all() #Cria a nova tabela
        flash("A tabela user nao foi encontrada e uma nova tabela foi gerada","danger")

    
    if form.validate_on_submit():
        email       = form.email.data      
        password    = form.password.data
        first_name  = form.first_name.data
        last_name   = form.last_name.data

        #checa para ver se o usuario ja existe. OBSOLETO, ESSA VERIFICACAO PODE JA EH FEITA NO PROPRIO form.validate_on_submit() --> def validate_email(self,email):
        # user = Users.query.filter_by(email = email).first() #Essa query do SQL retorna o usuario filtrado por email
        # if user:  #user é None se nao for encontrado, então é False.
            # flash(f"O email {user.email} já está registrado","danger")

        # else:
        user = Users(email = email, first_name = first_name, last_name = last_name) #cria um modelo de usuario para colocar no datatable
        user.set_password(password) #Essa funcao esta dentro do arquivo models.py
        db.session.add(user)
        db.session.commit()
        flash(f"O email {user.email} foi registrado com sucesso!","success")
        return redirect(url_for('index'))
    
    return render_template("register.html" , registerhl = True, form = form )


#%% Funcoes auxiliares ou de demonstracao


@app.route("/api")
@app.route("/api/<idx>")
def api(idx):
    if(idx == None):
        jdata = courseData
    else:
        jdata = courseData[int(idx)]
    
    return Response(json.dumps(jdata), mimetype = "application/json")



@app.route("/create_courses")
def create_courses():

    if 'courses' not in db.engine.table_names():
        db.create_all() 

    course = Courses(title = "foo1",description = "foo fighters",credits = 1,term = "sei la" )
    db.session.add(course)

    course = Courses(title = "foo2",description = "foo fighters2",credits = 2,term = "sei la2" )
    db.session.add(course)

    course = Courses(title = "foo3",description = "foo fighters3",credits = 2,term = "sei la3" )
    db.session.add(course)

    db.session.commit()


    flash('cursos registrado com sucesso','success')
    return render_template('index.html',indexhl = True)


#%% Modelo para gerar tabelas automaticamente caso elas nao estejam no database
#     if 'users' not in db.engine.table_names():
#         print('######################################## 2')
#         db.create_all() #Cria a nova tabela
#         flash("A tabela user nao foi encontrada e uma nova tabela foi gerada","danger")
#%%

# @app.route("/create_users")
# def create_users():

#     # Checa se a table já existe, se nao existir, cria uma nova.
#     if 'users' not in db.engine.table_names():
#         db.create_all() #Cria a nova tabela

#     #modelo de usuario para tentar criar no dataframe
#     usuario = Users(first_name="Plinio",last_name="Silva",email = "pliniobas@gmail.com",
#                     password = "123456",admin = False)
#     usuario.set_password(usuario.password)

#     # Checa nome de usuarios na tabela
#     bool_usuario_registrado = False
#     users = Users.query.all()
#     for user in users:
#         if user.email == usuario.email:
#             bool_usuario_registrado = True
#             print('encontrado usuario já registrado')

#     if not bool_usuario_registrado:
#         db.session.add(usuario)
#         db.session.commit()

#         users = Users.query.all()
#         for user in users:
#             if user.email == usuario.email:
#                 print('Registrado com sucesso %s'%user.email)
        

#     return render_template("user.html", users = users)