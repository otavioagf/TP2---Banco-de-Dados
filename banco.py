from Conection import Connect
import os

db = Connect("localhost", "banco", "postgres", "1234")

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def back():
    input("\nAperte Enter para voltar")

def add_pessoa():
    clear()
    print("----Adicionar Pessoa----")
    nome = input("Nome: ")
    cpf = input("CPF: ")
    data_nasc = input("Data de nascimento: ")
    edereco = input("Endereço: ")

    if db.manipulate(f"""
        INSERT INTO Pessoa(ID, Nome, CPF, DataNascimento, Endereco)
        VALUES ('{nome}', '{cpf}', '{data_nasc}', '{edereco}')
        """):
        print("Pessoa inserida com sucesso!")
    else:
        print("Erro ao inserir pessoa.")
    back()


def list_pessoa():
    clear()
    pessoas = db.consult("SELECT * FROM pessoa")
    if pessoas:
        for p in pessoas:
            print(p)
    else:
        print("Nenhuma pessoa encontrada.")
    back()

def menu_pessoa():
    while True:
        clear()
        print("---Menu Pessoas---")
        print("[1] - Adicionar")
        print("[2] - Listar")
        print("[0] - Sair")

        op = input("Opção: ")

        if op == 1 :
            add_pessoa()
        elif op == 2:
            list_pessoa()
        elif op == 0:
            break


def menu_inicial():
    while True:
        clear()