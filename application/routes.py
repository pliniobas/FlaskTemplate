from application import app #variavel app, dentro da pasta application/__init__.py
from flask import render_template, request

@app.route("/")
@app.route("/index")
@app.route("/home")
def index():
    return render_template("index.html", indexhl = True , logedin = True,)

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

@app.route("/login")
def login():

    for aux in request.args:
        print(request.args[aux])
        

    return render_template("login.html" , loginhl = True )

@app.route("/register",methods = ["GET","POST"])
def register():
    
    if request.method == "GET":
        print("parte do codigo que executarah quando chamar a pagina a sem preencher o form")
        pass

    if request.method == "POST": 
        print("essa parte so sera executada quando preencher o form")
        
        for aux in request.form: #request.form funciona como um dicionario.
            print( request.form[aux])
    
    return render_template("register.html" , registerhl = True )