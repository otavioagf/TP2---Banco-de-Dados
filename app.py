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
            return render_template("cliente_login.html", error = "Conta inválida")
    return render_template("cliente_login.html")

@app.route("/cliente/logout")
def cliente_logout():
    session.pop("conta_origem", None)
    flash("Você saiu da sua conta.", "info")
    return redirect(url_for("index"))

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
        telefone_pessoa = request.form["telefone_pessoa"].strip()

        try1 = db.manipulate(
                "INSERT INTO Conta(Tipo, Saldo, DataAbertura, Agencia_Id) VALUES(%s, %s, %s, %s)",
                (tipo_conta, 0, CURRENT_DATE, 1)
        )
        if not try1:
            return render_template("cadastra_cliente.html")
        
        row = db.consult("SELECT currval(pg_get_serial_sequence('Conta','numero'))")
        conta_numero = row[0][0]

        try2 = db.manipulate(
            "INSERT INTO Pessoa(Nome, CPF, DataNascimento, Endereco) VALUES (%s, %s, %s, %s)",
            (nome, cpf, data_nasc, endereco)
        )
        if not try2:
            flash("Erro ao criar Pessoa.", "error")
            return render_template("cadastra_cliente.html")

        row = db.consult("SELECT currval(pg_get_serial_sequence('Pessoa','id'))")
        pessoa_id = row[0][0]

        try3 = db.manipulate("INSERT INTO Cliente(pessoa_id) VALUES (%s)", (pessoa_id,))
        if not try3:
            flash("Erro ao criar Cliente.", "error")
            return render_template("cadastra_cliente.html")
        
        row = db.consult("SELECT currval(pg_get_serial_sequence('Pessoa','id'))")
        pessoa_id = row[0][0]

        try4 = db.manipulate(
            "INSERT INTO  Titularidade_conta(Cliente_pessoa_id, Conta_numero, DataVinculacao) VALUES (%s, %s, %s)",
            (pessoa_id, conta_numero, CURRENT_DATE)
            )
        if not try4:
            flash("Erro ao criar Cliente.", "error")
            return render_template("cadastra_cliente.html")
        
        try5 = db.manipulate(
            "INSERT INTO  TelefonePessoa(Pessoa_id, Telefone) VALUES (%s, %s)",
            (pessoa_id, telefone_pessoa)
            )
        if not try5:
            flash("Erro ao criar Telefone.", "error")
            return render_template("cadastra_cliente.html")

        flash(f"Conta criada com sucesso! Número: {conta_numero}", "success")
        return redirect(url_for("cliente_login"))
    return render_template("cadastra_cliente.html")

@app.route("/cliente/dados", methods=["GET"])
def cliente_dados():
    if "conta_origem" not in session:
        return redirect(url_for("cliente_login"))
    conta = session["conta_origem"]

    row = db.consult("""
            SELECT p.nome, p.cpf, p.endereco, p.datanascimento, c.numero, c.saldo, t.telefone
                     FROM conta c
                     JOIN titularidade_conta tc ON c.numero = tc.conta_numero
                     JOIN pessoa p ON tc.cliente_pessoa_id = p.id
                     LEFT JOIN telefonepessoa t ON p.id = t.pessoa_id
                     WHERE c.numero = %s
                     """, (conta,))
    
    if not row:
        return "Conta não existe", 404
    
    dados = {
        "nome": row[0][0],
        "cpf": row[0][1],
        "endereco": row[0][2],
        "data_nascimento": row[0][3],
        "numero_conta": row[0][4],
        "saldo": row[0][5],
        "telefone": row[0][6],
    }
    return render_template("cliente_dados.html", dados = dados)

@app.route("/cliente/transacao", methods=["GET", "POST"])
def cliente_transacao():
    if "conta_origem" not in session:
        return redirect(url_for("cliente_login"))

    if request.method == "POST":
        tipo = request.form["tipo"].strip().lower()
        valor = float(request.form["valor"])
        CURRENT_DATE = date.today()
        conta_origem = session["conta_origem"]

        if tipo == "transferencia":
            conta_destino = request.form["conta_destino"].strip()

            saldo_origem = db.consult(
                "SELECT Saldo FROM Conta WHERE Numero = %s", (conta_origem,)
            )

            if not saldo_origem or saldo_origem[0][0] < valor:
                flash("Saldo insuficiente.", "error")
                return render_template("cliente_transacao.html")


            ok_debita = db.manipulate(
                "UPDATE Conta SET Saldo = Saldo - %s WHERE Numero = %s",
                (valor, conta_origem)
            )
            if not ok_debita:
                flash("Erro ao debitar da conta de origem.", "error")
                return render_template("cliente_transacao.html")

            ok_credita = db.manipulate(
                "UPDATE Conta SET Saldo = Saldo + %s WHERE Numero = %s",
                (valor, conta_destino)
            )
            if not ok_credita:
                flash("Erro ao creditar na conta destino.", "error")
                return render_template("cliente_transacao.html")

            db.manipulate(
                "INSERT INTO Transacao (Data, Valor, Tipo, Descricao, Conta_Origem_Numero, Conta_Destino_Numero) "
                "VALUES (%s, %s, %s, %s, %s, %s)",
                (CURRENT_DATE, valor, "transferência", "Transferência Realizada", conta_origem, conta_destino)
            )
            flash("Transferência realizada!", "success")
            return redirect(url_for("menu_conta"))

        elif tipo == "deposito":
            conta_destino = conta_origem
            ok_credita = db.manipulate(
                "UPDATE Conta SET Saldo = Saldo + %s WHERE Numero = %s",
                (valor, conta_destino)
            )
            if ok_credita:
                db.manipulate(
                    "INSERT INTO Transacao (Data, Valor, Tipo, Descricao, Conta_Origem_Numero, Conta_Destino_Numero) "
                    "VALUES (%s, %s, %s, %s, %s, %s)",
                    (CURRENT_DATE, valor, "depósito", "Depósito Realizado", conta_destino, conta_destino)
                )
                flash("Depósito realizado!", "success")
                return redirect(url_for("menu_conta"))
            else:
                flash("Erro ao depositar.", "error")

        elif tipo == "saque":
            ok_debita = db.manipulate(
                "UPDATE Conta SET Saldo = Saldo - %s WHERE Numero = %s",
                (valor, conta_origem)
            )
            if ok_debita:
                db.manipulate(
                    "INSERT INTO Transacao (Data, Valor, Tipo, Descricao, Conta_Origem_Numero) "
                    "VALUES (%s, %s, %s, %s, %s)",
                    (CURRENT_DATE, valor, "saque", "Saque Realizado", conta_origem)
                )
                flash("Saque realizado!", "success")
                return redirect(url_for("menu_conta"))
            else:
                flash("Erro ao realizar saque.", "error")
        else:
            flash("Tipo de transação inválido.", "error")

    return render_template("cliente_transacao.html")

@app.route("/cliente/cartao", methods=["GET", "POST"])
def cliente_cartao():
    if "conta_origem" not in session:
        return redirect(url_for("cliente_login"))

    if request.method == "POST":
        tipo = request.form["tipo"].strip().lower()  
        conta = session["conta_origem"]
        ok = db.manipulate(
            "INSERT INTO Cartao (conta_numero, tipo, validade, bandeira) "
            "VALUES (%s, %s, %s, %s)",
            (conta, tipo, "03/2034", "VISA")
        )
        if ok:
            flash("Cartão gerado.", "success")
            return redirect(url_for("menu_conta"))
        flash("Erro ao gerar cartão.", "error")
    return render_template("cliente_cartao.html")

@app.route("/cliente/cartao_deleta", methods = ["GET", "POST"])
def cartao_deleta():
    if "conta_origem" not in session:
        return redirect(url_for("cliente_login"))
    conta = session["conta_origem"]

    if request.method == "POST":
        numero_cartao = request.form["numero_cartao"]
        db.manipulate("DELETE FROM Cartao WHERE Numero = %s AND Conta_numero = %s",(numero_cartao, conta))

    cartoes = db.consult("SELECT Numero, Tipo FROM Cartao WHERE Conta_numero = %s", (conta,))
    return render_template("cartao_deleta.html", cartoes = cartoes)


# ----------------- FUNCIONÁRIO -----------------
@app.route("/func/login", methods=["GET", "POST"])
def func_login():
    if request.method == "POST":
        mat = request.form["matricula"].strip()
        rows = db.consult("SELECT Matricula, Cargo FROM Funcionario WHERE Matricula = %s", (mat,))
        if rows:
            session["func_logado"] = mat
            session["cargo_logado"] = rows[0][1]
            if session["cargo_logado"].lower() == "gerente":
                return redirect(url_for("gerente_menu"))
            return redirect(url_for("func_menu"))
        flash("Funcionário inválido.", "error")
    return render_template("func_login.html")

@app.route("/func/logout")
def func_logout():
    session.pop("func_logado", None)
    session.pop("cargo_logado", None)
    flash("Logout efetuado.", "info")
    return redirect(url_for("index"))

@app.route("/func/menu")
def func_menu():
    if "func_logado" not in session or session.get("cargo_logado","").lower() == "gerente":
        return redirect(url_for("func_login"))
    return render_template("func_menu.html")

@app.route("/func/atendimento", methods=["GET", "POST"])
def func_atendimento():
    if "func_logado" not in session:
        return redirect(url_for("func_login"))

    if request.method == "POST":
        DATA_AT = date.today()
        cliente_id = request.form["cliente_id"].strip()
        descricao = request.form["descricao"].strip()
        ok = db.manipulate(
            "INSERT INTO Funcionario_Atende_Cliente(Funcionario_Pessoa_ID, Cliente_Pessoa_ID, DataAtendimento, Descricao_Atendimento) "
            "VALUES ( (SELECT Pessoa_ID FROM Funcionario WHERE Matricula = %s), %s, %s, %s)",
            (session["func_logado"], cliente_id, DATA_AT, descricao)
        )
        if ok:
            flash("Atendimento registrado.", "success")
            return redirect(url_for("func_menu"))
        else:
            flash("Falha ao registrar atendimento.", "error")
    return render_template("func_atendimento.html")

# ----------------- GERENTE -----------------
@app.route("/gerente/menu")
def gerente_menu():
    if "func_logado" not in session or session.get("cargo_logado","").lower() != "gerente":
        return redirect(url_for("func_login"))
    return render_template("gerente_menu.html")

@app.route("/gerente/lista_func")
def lista_func():
    if "func_logado" not in session or session.get("cargo_logado","").lower() != "gerente":
        return redirect(url_for("func_login"))
    mat_func = session["func_logado"]

    row = db.consult("SELECT Agencia_Id FROM Funcionario WHERE Matricula = %s", (mat_func,))
    agencia_id = row[0][0]

    funcs = db.consult("""
            SELECT f.matricula, p.nome
            FROM funcionario f
            JOIN pessoa p ON f.pessoa_id = p.id
            WHERE f.agencia_id = %s
                       """, (agencia_id,))
    return render_template("lista_func.html", funcs = funcs)

@app.route("/gerente/editar_func", methods=["GET", "POST"])
def gerente_editar_func():
    if "func_logado" not in session or session.get("cargo_logado","").lower() != "gerente":
        return redirect(url_for("func_login"))

    if request.method == "POST":
        mat_func = request.form["matricula"].strip()
        campo = request.form["campo"]

        if mat_func == session.get("func_logado"):

            if campo == "cargo":
                novo = request.form["novo_cargo"].strip()
                ok = db.manipulate("UPDATE Funcionario SET Cargo = %s WHERE Matricula = %s", (novo, mat_func))
            elif campo == "salario":
                novo = float(request.form["novo_salario"])
                ok = db.manipulate("UPDATE Funcionario SET Salario = %s WHERE Matricula = %s", (novo, mat_func))
            elif campo == "agencia":
                novo = int(request.form["nova_agencia"])
                ok = db.manipulate("UPDATE Funcionario SET Agencia_ID = %s WHERE Matricula = %s", (novo, mat_func))
            else:
                ok = False
        else:
            if campo == "cargo":
                novo = request.form["novo_cargo"].strip()
                ok = db.manipulate("UPDATE Funcionario SET Cargo = %s WHERE Matricula = %s", (novo, mat_func))
            elif campo == "salario":
                novo = float(request.form["novo_salario"])
                ok = db.manipulate("UPDATE Funcionario SET Salario = %s WHERE Matricula = %s", (novo, mat_func))
            elif campo == "agencia":
                novo = int(request.form["nova_agencia"])
                ok = db.manipulate("UPDATE Funcionario SET Agencia_ID = %s WHERE Matricula = %s", (novo, mat_func))
            else:
                ok = False
        if ok:
            flash("Dados do funcionário atualizados.", "success")
        else:
            flash("Erro ao atualizar funcionário.", "error")
        return redirect(url_for("gerente_menu"))

    return render_template("gerente_editar_func.html")

@app.route("/gerente/add_func", methods=["GET", "POST", "PUT"])
def gerente_add_func():
    if "func_logado" not in session or session.get("cargo_logado","").lower() != "gerente":
        return redirect(url_for("func_login"))
    if request.method == "POST":
        nome = request.form["nome"].strip()
        cpf = request.form["cpf"].strip()
        data_nasc = request.form["data_nasc"].strip()
        endereco = request.form["endereco"].strip()
        cargo = request.form["cargo"].strip()
        salario = request.form["salario"].strip()
        agencia = request.form["agencia_id"].strip()


        try1 = db.manipulate(
            "INSERT INTO Pessoa(Nome, CPF, DataNascimento, Endereco) VALUES (%s, %s, %s, %s)",
            (nome, cpf, data_nasc, endereco)
        )
        if not try1:
            flash("Erro ao criar Pessoa.", "error")
            return render_template("gerente_add_func.html")
        
        row = db.consult("SELECT currval(pg_get_serial_sequence('Pessoa','id'))")
        pessoa_id = row[0][0]

        try2 = db.manipulate(
                "INSERT INTO Funcionario(Pessoa_id, Matricula, Cargo, Salario,Agencia_Id) VALUES(%s, %s, %s, %s, %s)",
                (pessoa_id, 10, cargo, salario , agencia)
        )
        if not try2:
            return render_template("gerente_add_func.html")

        flash(f"Funcionário criado com sucesso!", "success")
        return redirect(url_for("gerente_menu"))
    return render_template("gerente_add_func.html")



@app.route("/func/editar_pessoal", methods=["GET", "POST"])
def func_editar_pessoal():
    if "func_logado" not in session or session.get("cargo_logado","").lower() == "gerente":
        return redirect(url_for("func_login"))

    if request.method == "POST":
        end_novo = request.form["endereco"].strip()
        ok = db.manipulate(
            "UPDATE Pessoa SET Endereco = %s "
            "WHERE ID = (SELECT Pessoa_ID FROM Funcionario WHERE Matricula = %s)",
            (end_novo, session["func_logado"])
        )
        if ok:
            flash("Endereço alterado!", "success")
            return redirect(url_for("func_menu"))
        flash("Erro ao alterar endereço.", "error")

    return render_template("func_editar_pessoal.html")

# -------------- RODAR --------------
if __name__ == "__main__":
    app.run(debug=True)

