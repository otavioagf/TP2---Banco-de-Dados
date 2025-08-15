from Conection import Connect
import os
from datetime import date
import random

db = Connect("localhost", "banco", "postgres", "1234")


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def back():
    input("\nAperte Enter para voltar")

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


def list_titular():
    clear()
    pessoas = db.consult("SELECT * FROM pessoa")
    if pessoas:
        for p in pessoas:
            print(p)
    else:
        print("Nenhuma pessoa encontrada.")
    back()

def realiza_transacao():
    clear()
    CURRENT_DATE = date.today()
    print("---Transação---")
    tipo = input("Tipo de Transação (deposito/saque/transferencia): ").strip().lower()
    valor = float(input("Valor: "))

    if tipo == "transferencia":
        conta_origem = input("Conta de origem: ")
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
        conta_destino = input("Conta de destino: ")

        if db.manipulate(f"""
            UPDATE Conta
            SET Saldo = Saldo + {valor}
            WHERE numero = '{conta_destino}'
                         """):
            db.manipulate(f"""
                INSERT INTO Transacao (Data, Valor, Tipo, Descricao, Conta_Origem_Numero, Conta_Destino_Numero)
                VALUES('{CURRENT_DATE}', {valor}, 'deposito', 'Depósito Realizado', {conta_destino}, {conta_destino})
                """)
            print("Depósito realizado!")
        else:
            print("Erro ao depositar.")
    elif tipo == 'saque':
        conta_origem = input("Conta de origem: ")

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
        print("---Menu Pessoas---")
        print("[1] - Adicionar")
        print("[2] - Listar")
        print("[0] - Sair")

        op = input("Opção: ")

        if op == "1" :
            add_conta()
        elif op == "2":
            list_titular()
        elif op == "0":
            break

def menu_func():
    while True:
        clear()
        print("---Área Funcionários---")
        print("[1] - Atendimento")
        print("[0] - Sair")

        op = input("Opção: ")

        if op == "1" :
            atendimento()
        elif op == "0":
            break

def menu_inicial():
    while True:
        clear()
        print("---Sistema Bancário---")
        print("[1] - Menu Contas")
        print("[0] - Sair")

        op = input("Opção: ")

        if op == "1" :
            menu_conta()
        elif op == "0":
            print("Fechando sistema")
            break


if __name__ == '__main__':
    menu_inicial()
    db.closing()