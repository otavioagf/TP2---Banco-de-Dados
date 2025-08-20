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
('Rafael Nunes', '91528347066', '2001-09-04', 'Rua F, 347');

INSERT INTO Cliente (Pessoa_ID) VALUES (1),
INSERT INTO Cliente (Pessoa_ID) VALUES (3),
INSERT INTO Cliente (Pessoa_ID) VALUES (5);

INSERT INTO Funcionario (Pessoa_ID, Matricula, Cargo, Salario, Agencia_ID) VALUES
(2, 'F001', 'Gerente', 7500.00, 1),
(4, 'F032', 'Gerente', 7500.00, 2),
(6, 'F006', 'Gerente', 7500.00, 3);

UPDATE Agencia SET Gerente_ID = 2 WHERE ID = 1,
UPDATE Agencia SET Gerente_ID = 4 WHERE ID = 2,
UPDATE Agencia SET Gerente_ID = 6 WHERE ID = 3;
INSERT INTO Conta (Tipo, Saldo, DataAbertura, Agencia_ID) VALUES
('Corrente', 543.00, CURRENT_DATE, 2),
('Corrente', 56.00, CURRENT_DATE, 1),
('Corrente', 2061.00, CURRENT_DATE, 3);

INSERT INTO Titularidade_Conta(Cliente_Pessoa_ID, Conta_Numero, DataVinculacao) VALUES
(1, 2, CURRENT_DATE),
(3, 1, CURRENT_DATE),
(5, 3, CURRENT_DATE);