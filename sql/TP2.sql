DROP SCHEMA public CASCADE;
CREATE SCHEMA public;

DROP VIEW IF EXISTS vw_cliente_idade;

DROP TABLE IF EXISTS Funcionario_Atende_Cliente;
DROP TABLE IF EXISTS Transacao;
DROP TABLE IF EXISTS Cartao;
DROP TABLE IF EXISTS Titularidade_Conta;
DROP TABLE IF EXISTS Conta;
DROP TABLE IF EXISTS Cliente;
DROP TABLE IF EXISTS Funcionario CASCADE;
DROP TABLE IF EXISTS TelefonePessoa;
DROP TABLE IF EXISTS TelefoneAgencia;
DROP TABLE IF EXISTS Agencia;
DROP TABLE IF EXISTS Pessoa;


CREATE TABLE Pessoa (
    ID SERIAL PRIMARY KEY,
    Nome VARCHAR(100) NOT NULL,
    CPF VARCHAR(11) NOT NULL UNIQUE,
    DataNascimento DATE NOT NULL,
    Endereco VARCHAR(150)
);

CREATE TABLE TelefonePessoa (
    Pessoa_ID INT NOT NULL,
    Telefone VARCHAR(20) NOT NULL,
    PRIMARY KEY (Pessoa_ID, Telefone),
    FOREIGN KEY (Pessoa_ID) REFERENCES Pessoa(ID)
);

CREATE TABLE Agencia (
    ID SERIAL PRIMARY KEY,
    Nome VARCHAR(100) NOT NULL,
    Endereco VARCHAR(150) NOT NULL,
    Estado CHAR(2) NOT NULL,
    Gerente_ID INT UNIQUE 
);

CREATE TABLE TelefoneAgencia (
    Agencia_ID INT NOT NULL,
    Telefone VARCHAR(20) NOT NULL,
    PRIMARY KEY (Agencia_ID, Telefone),
    FOREIGN KEY (Agencia_ID) REFERENCES Agencia(ID)
);

CREATE TABLE Funcionario (
    Pessoa_ID INT PRIMARY KEY,
    Matricula VARCHAR(8) NOT NULL UNIQUE,
    Cargo VARCHAR(50) NOT NULL,
    Salario DECIMAL(10, 2) NOT NULL,
    Agencia_ID INT NOT NULL, 
    CONSTRAINT fk_funcionario_pessoa FOREIGN KEY (Pessoa_ID) REFERENCES Pessoa(ID) ON DELETE CASCADE,
    CONSTRAINT fk_funcionario_agencia FOREIGN KEY (Agencia_ID) REFERENCES Agencia(ID) ON DELETE RESTRICT
);

ALTER TABLE Agencia ADD CONSTRAINT fk_agencia_gerente FOREIGN KEY (Gerente_ID) REFERENCES Funcionario(Pessoa_ID) ON DELETE SET NULL;

CREATE TABLE Cliente (
    Pessoa_ID INT PRIMARY KEY,
    CONSTRAINT fk_cliente_pessoa FOREIGN KEY (Pessoa_ID) REFERENCES Pessoa(ID) ON DELETE CASCADE
);

CREATE TABLE Conta (
    Numero INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    Tipo VARCHAR(20) NOT NULL CHECK (Tipo IN ('Corrente', 'Poupança')),
    Saldo DECIMAL(12, 2) NOT NULL DEFAULT 0.00,
    DataAbertura DATE NOT NULL,
    Agencia_ID INT NOT NULL,
    CONSTRAINT fk_conta_agencia FOREIGN KEY (Agencia_ID) REFERENCES Agencia(ID) ON DELETE RESTRICT
);


CREATE TABLE Titularidade_Conta (
    Cliente_Pessoa_ID INT NOT NULL,
    Conta_Numero INT NOT NULL,
    DataVinculacao DATE NOT NULL,
    PRIMARY KEY (Cliente_Pessoa_ID, Conta_Numero), 
    CONSTRAINT fk_titularidade_cliente FOREIGN KEY (Cliente_Pessoa_ID) REFERENCES Cliente(Pessoa_ID) ON DELETE CASCADE,
    CONSTRAINT fk_titularidade_conta FOREIGN KEY (Conta_Numero) REFERENCES Conta(Numero) ON DELETE CASCADE
);


CREATE TABLE Cartao (
    Numero BIGINT GENERATED ALWAYS AS IDENTITY,
    Conta_Numero INT NOT NULL, 
    Tipo VARCHAR(20) NOT NULL, 
    Validade VARCHAR(7) NOT NULL, 
    Bandeira VARCHAR(30) NOT NULL,
    PRIMARY KEY (Numero, Conta_Numero), 
    CONSTRAINT fk_cartao_conta FOREIGN KEY (Conta_Numero) REFERENCES Conta(Numero) ON DELETE CASCADE
);


CREATE TABLE Transacao (
    ID SERIAL PRIMARY KEY,
    Data TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    Valor DECIMAL(12, 2) NOT NULL,
    Tipo VARCHAR(20) NOT NULL CHECK (Tipo IN ('Saque', 'Depósito', 'Transferência')), 
    Descricao VARCHAR(200),
    Conta_Origem_Numero INT NOT NULL,
    Conta_Destino_Numero INT,
    
    CONSTRAINT fk_transacao_conta_origem FOREIGN KEY (Conta_Origem_Numero) REFERENCES Conta(Numero) ON DELETE RESTRICT,
    CONSTRAINT fk_transacao_conta_destino FOREIGN KEY (Conta_Destino_Numero) REFERENCES Conta(Numero) ON DELETE RESTRICT,
    CHECK (Conta_Origem_Numero <> Conta_Destino_Numero)
);


CREATE TABLE Funcionario_Atende_Cliente (
    Funcionario_Pessoa_ID INT NOT NULL,
    Cliente_Pessoa_ID INT NOT NULL,
    DataAtendimento TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    Descricao_Atendimento TEXT,
    PRIMARY KEY (Funcionario_Pessoa_ID, Cliente_Pessoa_ID, DataAtendimento), 
    CONSTRAINT fk_atende_funcionario FOREIGN KEY (Funcionario_Pessoa_ID) REFERENCES Funcionario(Pessoa_ID) ON DELETE NO ACTION,
    CONSTRAINT fk_atende_cliente FOREIGN KEY (Cliente_Pessoa_ID) REFERENCES Cliente(Pessoa_ID) ON DELETE CASCADE
);

CREATE VIEW vw_cliente_idade AS
SELECT
    Pessoa.ID,
    Pessoa.Nome,
    EXTRACT(YEAR FROM AGE(CURRENT_DATE, Pessoa.DataNascimento)) AS Idade
FROM Pessoa
INNER JOIN Cliente ON Pessoa.ID = Cliente.Pessoa_ID;
