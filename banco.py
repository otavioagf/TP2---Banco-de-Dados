#Era o arquivo principal, mas depois virou o outro por causa do frontend, então pode ser ignorado esse


from Conection import Connect
import os
from datetime import date
import random

db = Connect("localhost", "banco", "postgres", "1234")


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def back():
    input("\nAperte Enter para voltar")

"""---------Área Cliente---------"""

def login():
    global conta_origem
    clear()
    print("---Login---")
    num_conta = input("Número da conta: ")

    result = db.consult(f"""
                SELECT Numero
                FROM Conta
                WHERE Numero = '{num_conta}'
                        """)
    if result:
        conta_origem = num_conta
        print("Login realizado com sucesso!")
        menu_conta()
    else:
        print("Conta inválida")
    back()


def add_conta():
    clear()
    CURRENT_DATE = date.today()
    numero = random.randint(100000, 999999)
    print("----Criar conta----")
    nome = input("Nome: ")
    cpf = input("CPF: ")
    data_nasc = input("Data de nascimento: ")
    edereco = input("Endereço: ")
    tipo_conta = input("Tipo de conta: ")

    if db.manipulate(f"""
        INSERT INTO Conta(Numero, Tipo, Saldo, DataAbertura, Agencia_Id)
        VALUES ('{numero}', '{tipo_conta}', '{0}', '{CURRENT_DATE}', '{1}')
        """):
        
        
        if db.manipulate(f"""
            INSERT INTO Pessoa(Nome, CPF, DataNascimento, Endereco)
            VALUES ('{nome}', '{cpf}', '{data_nasc}', '{edereco}')
            RETURNING ID
            """):
            pessoa_id = db.consult("""
                        SELECT currval(pg_get_serial_sequence('Pessoa', 'id'))
                        """)[0][0]
            
            if db.manipulate(f"""
            INSERT INTO Cliente(pessoa_id)
            VALUES({pessoa_id})
            """):
                
                print("Conta criada com sucesso!")
        else:
            print("Erro ao criar conta")
    else:
        print("Não foi possível continuar a operação")
    back()


def list_titulares():
    clear()
    pessoas = db.consult("SELECT * FROM pessoa")
    if pessoas:
        for p in pessoas:
            print(p)
    else:
        print("Nenhuma pessoa encontrada.")
    back()

def realiza_transacao():
    global conta_origem
    clear()
    CURRENT_DATE = date.today()
    print("---Transação---")
    tipo = input("Tipo de Transação (deposito/saque/transferencia): ").strip().lower()
    valor = float(input("Valor: "))

    if tipo == "transferencia":
        conta_destino = input("Conta de destino: ")

        if db.manipulate(f"""
            UPDATE Conta
            SET Saldo = Saldo - {valor}
            WHERE Numero = '{conta_origem}'
            """):
            if db.manipulate(f"""
            UPDATE Conta
            SET Saldo = Saldo + {valor}
            WHERE Numero = '{conta_destino}'
            """):
                
                db.manipulate(f"""
                    INSERT INTO Transacao (Data, Valor, Tipo, Descricao, Conta_Origem_Numero, Conta_Destino_Numero)
                    VALUES('{CURRENT_DATE}', {valor}, 'transferencia', 'Transferência Realizada', {conta_origem}, {conta_destino})
                    """)
                print("Transferência realizada!")
            else:
                print("Erro ao creditar na conta destino.")
        else:
            print("Erro ao debitar da conta de origem.")
    elif tipo == 'deposito':
        conta_destino = conta_origem

        if db.manipulate(f"""
            UPDATE Conta
            SET Saldo = Saldo + {valor}
            WHERE numero = '{conta_destino}'
                         """):
            db.manipulate(f"""
                INSERT INTO Transacao (Data, Valor, Tipo, Descricao, Conta_Origem_Numero, Conta_Destino_Numero)
                VALUES('{CURRENT_DATE}', {valor}, 'deposito', 'Depósito Realizado', {conta_origem}, {conta_destino})
                """)
            print("Depósito realizado!")
        else:
            print("Erro ao depositar.")
    elif tipo == 'saque':

        if db.manipulate(f"""
            UPDATE Conta
            SET Saldo = Saldo - {valor}
            WHERE Numero = '{conta_origem}'
            """):
            db.manipulate(f"""
                INSERT INTO Transacao (Data, Valor, Tipo, Descricao, Conta_Origem_Numero)
                VALUES('{CURRENT_DATE}', {valor}, 'saque', 'Saque Realizado', {conta_origem})
                """)
            print("Saque realizado!")
        else:
            print("Erro ao realizar saque.")
    else:
        print("Transação inválida.")
    back()

def gera_cartao():
    global conta_origem
    clear()
    print("---Cartões---")

    tipo_cartao = input("Tipo cartão (debito/credito)")

    if db.manipulate(f"""
        INSERT INTO Cartao(conta_numero, tipo, validade, bandeira)
        VALUES({conta_origem}, '{tipo_cartao}', '03/2030', 'VISA' )            
                     """):
        print("Cartão Gerado")
    else:
        print("Erro ao gerar cartão.")
    back()
        

"""---------Área Funcionário---------"""

def login_func():
    global func_logado, cargo_logado
    clear()
    print("---Login---")
    mat_func = input("Matrícula do funcionário: ")

    result = db.consult(f"""
                SELECT Matricula, cargo
                FROM Funcionario
                WHERE Matricula = '{mat_func}'
                        """)
    if result:
        func_logado = mat_func
        cargo_logado = result[0]['cargo']
        if cargo_logado.lower() == 'gerente':
            menu_gerente()
        else:
            menu_func()
    else:
        print("Conta inválida")
    back()


def edita_func():
    global func_logado, cargo_logado
    clear()

    if cargo_logado.lower()== 'gerente':
        mat_func = input("Funcionário a ser editado: ")
        print("O que será editado:")
        print("[1] - Cargo")
        print("[2] - Salário")
        print("[3] - Agência")
        print("[0] - Voltar")
        
        op = input("Opção: ")
        if op == "1":
            cargo_novo = input("Novo cargo: ")
            if db.manipulate(f"""
                UPDATE Funcionario
                SET Cargo = '{cargo_novo}'
                WHERE matricula = {mat_func}
                             """):
                print("Cargo alterado!")
            else:
                print("Erro ao alterar cargo.")
            back()
        elif op == "2":
            sal_novo = input("Novo salário: ")
            if db.manipulate(f"""
                UPDATE Funcionario
                SET Salario = {sal_novo}
                WHERE matricula = {mat_func}
                             """):
                print("Salário alterado!")
            else:
                print("Erro ao alterar salário.")
            back()
        elif op == "3":
            ag_id = input("Nova agência: ")
            if db.manipulate(f"""
                UPDATE Funcionario
                SET Agencia_Id = {ag_id}
                WHERE matricula = {mat_func}
                             """):
                print("Agência alterada!")
            else:
                print("Erro ao alterar agência.")
            back()
        elif op == "0":
            back()
    else:
        print("O que será editado:")
        print("[1] - Endereço")
        print("[0] - Voltar")

        op = input("Opção: ")

        if op == "1":
            end_novo = input("Novo endereço: ")
            if db.manipulate(f"""
                UPDATE Pessoa
                SET Endereco = '{end_novo}'
                WHERE id = (
                    SELECT pessoa_id
                    FROM funcionario
                    WHERE matricula = '{func_logado}'
                )
                """):
                print("Endereço alterado!")
            else:
                print("Erro ao alterar endereço")
            back()
        elif op == "0":
            back()
                
            

def atendimento():
    clear()
    print("---Realizar Atendimento---")
    DATA_ATENDIMENTO = date.today()
    cliente_id = input("Cliente atendido: ")
    descricao = input("Assunto do atendimento: ")

    if db.manipulate(f"""
        INSERT INTO Funcionario_atende_cliente(Funcionario_id, Cliente_id, DataAtendimento, Descricao)
        VALUES('{1}', '{cliente_id}', '{DATA_ATENDIMENTO}', '{descricao}')
                     """):
        print("Cadastro de Atendimento concluído!")
    else:
        print("Cadastro Atendimento falhou.")
    back()


"""-------------------Menus---------------------"""


def menu_conta():
    while True:
        clear()
        print("---Menu Conta---")
        print("[1] - Transferência")
        print("[2] - Gerar Cartão")
        print("[0] - Sair")

        op = input("Opção: ")

        if op == "1" :
            realiza_transacao()
        elif op == "2":
            gera_cartao()
        elif op == "0":
            break

def menu_func():
    while True:
        clear()
        print("---Área Funcionários---")
        print("[1] - Atendimento")
        print("[2] - Editar informações pessoais")
        print("[0] - Sair")

        op = input("Opção: ")

        if op == "1" :
            atendimento()
        elif op == "2":
            edita_func()
        elif op == "0":
            break

def menu_gerente():
    while True:
        clear()
        print("---Área Gerente---")
        print("[1] - Editar um funcionário")
        print("[0] - Sair")
        op = input("Opção: ")

        if op == "1" :
            edita_func()
        elif op == "0":
            print("Fechando sistema")
            break

def menu_login():
    while True:
        clear()
        print("---Login---")
        print("[1] - Cliente")
        print("[2] - Cadastrar como cliente")
        print("[3] - Funcionário")
        print("[0] - Sair")

        op = input("Opção: ")

        if op == "1" :
            login()
        elif op == "2":
            add_conta()
        elif op == "3":
            login_func()
        elif op == "0":
            break

def menu_inicial():
    while True:
        clear()
        print("---Sistema Bancário---")
        print("[1] - Login")
        print("[0] - Sair")

        op = input("Opção: ")

        if op == "1" :
            menu_login()
        elif op == "0":
            print("Fechando sistema")
            break


if __name__ == '__main__':
    menu_inicial()
    db.closing()