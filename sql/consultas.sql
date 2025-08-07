-- CONSULTAS PARA O TRABALHO PRÁTICO 2

-- Consulta 1: Listar todos os clientes e suas respectivas idades, ordenando do mais velho para o mais novo.
-- Demonstra o uso da VIEW para atributos derivados.
SELECT Nome, Idade FROM vw_cliente_idade ORDER BY Idade DESC;

-- Consulta 2: Mostrar cada agência e o nome do seu gerente.
-- Demonstra o JOIN entre as tabelas Agencia, Funcionario e Pessoa.
SELECT 
    a.Nome AS Nome_Agencia,
    p.Nome AS Nome_Gerente
FROM Agencia a
LEFT JOIN Funcionario f ON a.Gerente_ID = f.Pessoa_ID
LEFT JOIN Pessoa p ON f.Pessoa_ID = p.ID;

-- Consulta 3: Listar todas as contas com saldo acima de R$ 5000,00, mostrando o nome do primeiro titular e o nome da agência.
SELECT 
    p.Nome as Nome_Titular,
    c.Numero as Numero_Conta,
    c.Saldo,
    ag.Nome as Nome_Agencia
FROM Conta c
JOIN Titularidade_Conta tc ON c.Numero = tc.Conta_Numero
JOIN Cliente cl ON tc.Cliente_Pessoa_ID = cl.Pessoa_ID
JOIN Pessoa p ON cl.Pessoa_ID = p.ID
JOIN Agencia ag ON c.Agencia_ID = ag.ID
WHERE c.Saldo > 5000.00;

-- Adicione aqui quantas consultas forem necessárias para o trabalho...