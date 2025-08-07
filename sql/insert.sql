-- Inserindo Agências
INSERT INTO Agencia (Nome, Endereco, Estado) VALUES 
('Agência Centro JM', 'Av. Getúlio Vargas, 100', 'MG'),
('Agência Bairro Novo', 'Rua das Flores, 550', 'MG');

-- Inserindo Pessoas
INSERT INTO Pessoa (Nome, CPF, DataNascimento, Endereco) VALUES
('João Silva', '11122233344', '1990-05-15', 'Rua A, 123'),
('Maria Oliveira', '55566677788', '1985-11-20', 'Rua B, 456'),
('Carlos Pereira', '99988877766', '1995-02-10', 'Rua C, 789');

-- Inserindo um Cliente (João Silva, ID=1)
INSERT INTO Cliente (Pessoa_ID) VALUES (1);

-- Inserindo um Funcionário (Maria Oliveira, ID=2) que trabalha na Agência (ID=1)
INSERT INTO Funcionario (Pessoa_ID, Matricula, Cargo, Salario, Agencia_ID) VALUES
(2, 'F001', 'Gerente', 7500.00, 1);

-- Atualizando a Agência para definir o gerente
UPDATE Agencia SET Gerente_ID = 2 WHERE ID = 1;