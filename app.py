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
