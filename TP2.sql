-- Remove a view se existir
DROP VIEW IF EXISTS vw_cliente_idade;

-- Remove as tabelas em ordem reversa de dependência, com CASCADE onde necessário
DROP TABLE IF EXISTS Funcionario_Atende_Cliente;
DROP TABLE IF EXISTS Transacao;
DROP TABLE IF EXISTS Cartao;
DROP TABLE IF EXISTS Titularidade_Conta;
DROP TABLE IF EXISTS Conta;
DROP TABLE IF EXISTS Cliente;
DROP TABLE IF EXISTS Funcionario CASCADE;
DROP TABLE IF EXISTS Agencia;
DROP TABLE IF EXISTS Pessoa;


-- Tabela base para a generalização.
-- Contém os atributos comuns a Clientes e Funcionários. [cite: 113, 114]
CREATE TABLE Pessoa (
    ID SERIAL PRIMARY KEY,
    Nome VARCHAR(100) NOT NULL,
    CPF VARCHAR(11) NOT NULL UNIQUE,
    DataNascimento DATE NOT NULL,
    Endereco VARCHAR(150)
    -- O atributo derivado 'Idade' é calculado pela aplicação e não armazenado. [cite: 114]
);

-- Tabela para Agências Bancárias. [cite: 120, 121]
CREATE TABLE Agencia (
    ID SERIAL PRIMARY KEY,
    Nome VARCHAR(100) NOT NULL,
    Endereco VARCHAR(150) NOT NULL,
    Estado CHAR(2) NOT NULL,
    -- A relação 'Gerencia' (1:1) será definida após a criação da tabela Funcionario.
    -- Vamos adicionar a coluna aqui e a restrição de chave estrangeira depois.
    Gerente_ID INT UNIQUE -- UNIQUE garante que um funcionário só pode gerenciar uma agência.
);

-- Subclasse Funcionário, herda de Pessoa. [cite: 118, 119]
-- Um funcionário está vinculado a uma agência. [cite: 34]
CREATE TABLE Funcionario (
    Pessoa_ID INT PRIMARY KEY,
    Matricula VARCHAR(8) NOT NULL UNIQUE,
    Cargo VARCHAR(50) NOT NULL,
    Salario DECIMAL(10, 2) NOT NULL,
    Agencia_ID INT NOT NULL, -- Relacionamento 'Trabalha' (Funcionário N:1 Agência) [cite: 51, 86]
    CONSTRAINT fk_funcionario_pessoa FOREIGN KEY (Pessoa_ID) REFERENCES Pessoa(ID) ON DELETE CASCADE,
    CONSTRAINT fk_funcionario_agencia FOREIGN KEY (Agencia_ID) REFERENCES Agencia(ID) ON DELETE RESTRICT
);

-- Agora que Funcionario existe, podemos adicionar a restrição de chave estrangeira para o gerente.
-- Isso resolve o problema de dependência circular na criação das tabelas.
ALTER TABLE Agencia ADD CONSTRAINT fk_agencia_gerente FOREIGN KEY (Gerente_ID) REFERENCES Funcionario(Pessoa_ID) ON DELETE SET NULL;

-- Subclasse Cliente, herda de Pessoa. [cite: 115]
CREATE TABLE Cliente (
    Pessoa_ID INT PRIMARY KEY,
    CONSTRAINT fk_cliente_pessoa FOREIGN KEY (Pessoa_ID) REFERENCES Pessoa(ID) ON DELETE CASCADE
);
-- A restrição de disjunção (um Pessoa_ID não pode estar em Cliente e Funcionario ao mesmo tempo)
-- é garantida implicitamente. Um ID só pode ser usado uma vez como chave primária.

-- Tabela Contas Bancárias.
-- Cada conta pertence a uma agência. [cite: 33, 123]
CREATE TABLE Conta (
    Numero INT PRIMARY KEY,
    Tipo VARCHAR(20) NOT NULL CHECK (Tipo IN ('Corrente', 'Poupança')),
    Saldo DECIMAL(12, 2) NOT NULL DEFAULT 0.00,
    DataAbertura DATE NOT NULL,
    Agencia_ID INT NOT NULL,
    CONSTRAINT fk_conta_agencia FOREIGN KEY (Agencia_ID) REFERENCES Agencia(ID) ON DELETE RESTRICT
);

-- Tabela associativa para o relacionamento N:N entre Cliente e Conta (Titularidade). [cite: 47, 125]
CREATE TABLE Titularidade_Conta (
    Cliente_Pessoa_ID INT NOT NULL,
    Conta_Numero INT NOT NULL,
    DataVinculacao DATE NOT NULL,
    PRIMARY KEY (Cliente_Pessoa_ID, Conta_Numero), -- Chave primária composta
    CONSTRAINT fk_titularidade_cliente FOREIGN KEY (Cliente_Pessoa_ID) REFERENCES Cliente(Pessoa_ID) ON DELETE CASCADE,
    CONSTRAINT fk_titularidade_conta FOREIGN KEY (Conta_Numero) REFERENCES Conta(Numero) ON DELETE CASCADE
);

-- Tabela para Cartões (Entidade Fraca). [cite: 42, 128]
-- A existência de um cartão depende da existência de uma conta.
CREATE TABLE Cartao (
    Numero VARCHAR(16) NOT NULL,
    Conta_Numero INT NOT NULL, -- Chave estrangeira para a entidade "dona"
    Tipo VARCHAR(20) NOT NULL, -- Débito ou Crédito [cite: 129]
    Validade VARCHAR(7) NOT NULL, -- Formato MM/AAAA
    Bandeira VARCHAR(30) NOT NULL,
    PRIMARY KEY (Numero, Conta_Numero), -- Chave primária composta para identificar unicamente o cartão no contexto da conta
    CONSTRAINT fk_cartao_conta FOREIGN KEY (Conta_Numero) REFERENCES Conta(Numero) ON DELETE CASCADE
);

-- ===================================================================
-- AJUSTES COM BASE NO FEEDBACK DO PROFESSOR
-- ===================================================================

-- 1. Tabela de Transações (MODELO CORRIGIDO)
-- Corrige a ambiguidade de quem envia e quem recebe. [cite: 130, 131, 133, 134]
CREATE TABLE Transacao (
    ID SERIAL PRIMARY KEY,
    Data TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    Valor DECIMAL(12, 2) NOT NULL,
    Tipo VARCHAR(20) NOT NULL CHECK (Tipo IN ('Saque', 'Depósito', 'Transferência')), -- Corrigido: adicionada vírgula no final
    Descricao VARCHAR(200),
    
    -- Chave estrangeira para a conta que realiza a transação (origem).
    -- Para saques e transferências, esta é a conta de onde o dinheiro sai.
    -- Para depósitos, é a conta que recebe o dinheiro.
    Conta_Origem_Numero INT NOT NULL,
    
    -- Chave estrangeira para a conta de destino (APENAS para transferências).
    -- Será NULL para saques e depósitos.
    Conta_Destino_Numero INT,
    
    CONSTRAINT fk_transacao_conta_origem FOREIGN KEY (Conta_Origem_Numero) REFERENCES Conta(Numero) ON DELETE RESTRICT,
    CONSTRAINT fk_transacao_conta_destino FOREIGN KEY (Conta_Destino_Numero) REFERENCES Conta(Numero) ON DELETE RESTRICT,

    -- Garante que em uma transferência, a conta de origem e destino não sejam a mesma.
    CHECK (Conta_Origem_Numero <> Conta_Destino_Numero)
);

-- 2. Tabela Associativa para o relacionamento "Atende" (NOVA TABELA)
-- Implementa a relação N:N onde um funcionário pode atender múltiplos clientes,
-- e um cliente pode ser atendido por múltiplos funcionários.
CREATE TABLE Funcionario_Atende_Cliente (
    Funcionario_Pessoa_ID INT NOT NULL,
    Cliente_Pessoa_ID INT NOT NULL,
    DataAtendimento TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    Descricao_Atendimento TEXT,
    
    PRIMARY KEY (Funcionario_Pessoa_ID, Cliente_Pessoa_ID, DataAtendimento), -- Chave composta para permitir múltiplos atendimentos ao longo do tempo
    CONSTRAINT fk_atende_funcionario FOREIGN KEY (Funcionario_Pessoa_ID) REFERENCES Funcionario(Pessoa_ID) ON DELETE NO ACTION,
    CONSTRAINT fk_atende_cliente FOREIGN KEY (Cliente_Pessoa_ID) REFERENCES Cliente(Pessoa_ID) ON DELETE CASCADE
);

-- View que calcula a idade dos clientes com base na data atual e data de nascimento
CREATE VIEW vw_cliente_idade AS
SELECT
    Pessoa.ID,
    Pessoa.Nome,
    EXTRACT(YEAR FROM AGE(CURRENT_DATE, Pessoa.DataNascimento)) AS Idade
FROM Pessoa
INNER JOIN Cliente ON Pessoa.ID = Cliente.Pessoa_ID;
