from flask import Flask, render_template, request, redirect, url_for, session, flash
from Conection import Connect
from datetime import date
import random

app = Flask(__name__)
app.secret_key = "123"
db = Connect("localhost", "banco", "postgres", "1234")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login_menu")
def login_menu():
    return render_template("login_menu.html")

@app.route("/cliente/login", methods = ["GET", "POST"])
def cliente_login():
    if request.method == "POST":
        conta_logada = request.form["conta"].strip()
        rows = db.consult("SELECT Numero FROM Conta WHERE Numero = %s", (conta_logada,))

        if rows:
            session["conta_origem"] = conta_logada
            return redirect(url_for("menu_conta"))
        else:
            return render_template("login.html", error = "Conta inválida")
    return render_template("login.html")

@app.route("/menu_conta")
def menu_conta():
    if "conta_origem" not in session:
        return redirect(url_for("cliente_login"))
    conta = session["conta_origem"]
    return render_template("menu_conta.html", conta = conta)

@app.route("/cliente/cadastro", methods = ["GET", "POST"])
def cadastra_cliente():
    if request.method == "POST":
        CURRENT_DATE = date.today()
        nome = request.form["nome"].strip()
        cpf = request.form["cpf"].strip()
        data_nasc = request.form["data_nasc"].strip()
        endereco = request.form["endereco"].strip()
        tipo_conta = request.form["tipo_conta"].strip()

        try1 = db.manipulate(
                "INSERT INTO Conta(Tipo, Saldo, DataAbertura, Agencia_Id) VALUES(%s, %s, %s, %s)",
                (tipo_conta, 0, CURRENT_DATE, 1)
        )
        if not try1:
            return render_template("cadastra_cliente.html")
        
        row = db.consult("SELECT currval(pg_get_serial_sequence('Pessoa','id'))")
        pessoa_id = row[0][0]


