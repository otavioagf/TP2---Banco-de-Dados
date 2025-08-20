DELETE FROM Transacao;
DELETE FROM Cartao;
DELETE FROM Titularidade_Conta;
DELETE FROM Conta;
DELETE FROM Funcionario_Atende_Cliente;
DELETE FROM Cliente;
DELETE FROM Agencia;
DELETE FROM Pessoa;
DELETE FROM Funcionario;
DELETE FROM Pessoa;
DELETE FROM TelefonePessoa;
DELETE FROM TelefoneAgencia;


INSERT INTO Agencia (Nome, Endereco, Estado) VALUES 
('Agência Centro JM', 'Av. Getúlio Vargas, 100', 'MG'),
('Agência Bairro Novo', 'Rua das Flores, 550', 'MG'),
('Agência Treze Dois', 'Avenida Santo Amaro, 200', 'MG'),
('Agência Velha Cidade', 'Rua das Torres, 2715', 'MG');

INSERT INTO Pessoa (Nome, CPF, DataNascimento, Endereco) VALUES
('João Silva', '11122233344', '1990-05-15', 'Rua A, 123'),
('Maria Oliveira', '55566677788', '1985-11-20', 'Rua B, 456'),
('Carlos Pereira', '99988877766', '1995-02-10', 'Rua C, 789'),
('Lucas Andrade', '48217690532', '1987-11-23', 'Rua D, 563'),
('Mariana Costa', '03759468219', '1993-06-15', 'Rua E, 865'),
('Rafael Nunes', '91528347066', '2001-09-04', 'Rua F, 347'),
('Ana Clara', '12345678901', '1998-07-22', 'Av. Principal, 1010'),
('Bruno Rocha', '23456789012', '1982-01-30', 'Rua da Passagem, 987'),
('Fernanda Lima', '34567890123', '2000-03-12', 'Alameda dos Anjos, 45'),
('Ricardo Souza', '45678901234', '1975-12-01', 'Travessa do Sol, 15');


INSERT INTO Cliente (Pessoa_ID) VALUES (1), (3), (5), (7), (9);

INSERT INTO Funcionario (Pessoa_ID, Matricula, Cargo, Salario, Agencia_ID) VALUES
(2, 'F001', 'Gerente', 7500.00, 1),
(4, 'F032', 'Gerente', 7500.00, 2),
(6, 'F006', 'Caixa', 3200.00, 1),
(8, 'F015', 'Atendente', 2800.00, 2),
(10, 'F022', 'Gerente', 8200.00, 3);

UPDATE Agencia SET Gerente_ID = 2 WHERE ID = 1;
UPDATE Agencia SET Gerente_ID = 4 WHERE ID = 2;
UPDATE Agencia SET Gerente_ID = 10 WHERE ID = 3;

INSERT INTO TelefonePessoa(Pessoa_ID, Telefone) VALUES
(1, '97323-1545'),
(2, '97323-1545'),
(6, '97323-1545'),
(5, '97323-1545'),
(3, '97323-1545');


INSERT INTO TelefoneAgencia(Agencia_ID, Telefone) VALUES
(1, '98992-4003'),
(2, '96522-7418'),
(3, '96412-5798'),
(4, '95422-6434');

INSERT INTO Conta (Tipo, Saldo, DataAbertura, Agencia_ID) VALUES
('Corrente', 1500.75, '2022-08-10', 1), 
('Poupança', 12500.00, '2021-03-20', 2), 
('Corrente', 850.25, '2023-01-15', 1), 
('Corrente', 25000.50, '2020-11-05', 3), 
('Poupança', 2300.00, '2023-05-30', 2);


INSERT INTO Titularidade_Conta(Cliente_Pessoa_ID, Conta_Numero, DataVinculacao) VALUES
(1, 1, '2022-08-10'), 
(3, 2, '2021-03-20'), 
(5, 3, '2023-01-15'), 
(7, 4, '2020-11-05'), 
(9, 5, '2023-05-30'); 

INSERT INTO Cartao(Conta_Numero, Tipo, Validade, Bandeira) VALUES
(1, 'Débito', '10/2028', 'Mastercard'),
(2, 'Crédito', '12/2027', 'Visa'),
(4, 'Crédito', '08/2029', 'Visa'),
(4, 'Débito', '08/2029', 'Elo');

INSERT INTO Transacao (Data, Valor, Tipo, Descricao, Conta_Origem_Numero, Conta_Destino_Numero) VALUES
('2025-08-15 10:30:00', 200.00, 'Saque', 'Saque em caixa eletrônico', 1, NULL),
('2025-08-18 14:00:00', 500.00, 'Depósito', 'Depósito em dinheiro', 2, NULL),
('2025-08-19 09:15:00', 150.50, 'Transferência', 'Transferência para João S.', 4, 1),
('2025-08-20 11:00:00', 800.00, 'Transferência', 'Pagamento de aluguel', 5, 2);


INSERT INTO Funcionario_Atende_Cliente(Funcionario_Pessoa_ID, Cliente_Pessoa_ID, DataAtendimento, Descricao_Atendimento) VALUES
(6, 1, '2025-08-10 15:00:00', 'Abertura de conta e dúvidas sobre taxas.'),
(8, 5, '2025-08-12 11:20:00', 'Solicitação de novo cartão de débito.');