SELECT Nome, Idade FROM vw_cliente_idade ORDER BY Idade DESC;


SELECT 
    a.Nome AS Nome_Agencia,
    p.Nome AS Nome_Gerente
FROM Agencia a
LEFT JOIN Funcionario f ON a.Gerente_ID = f.Pessoa_ID
LEFT JOIN Pessoa p ON f.Pessoa_ID = p.ID;


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


SELECT 
    a.Nome AS Nome_Agencia,
    COUNT(f.Pessoa_ID) AS Quantidade_Funcionarios
FROM Agencia a
JOIN Funcionario f ON a.ID = f.Agencia_ID
GROUP BY a.Nome
ORDER BY Quantidade_Funcionarios DESC;


SELECT 
    a.Nome AS Nome_Agencia,
    SUM(c.Saldo) AS Saldo_Total_Consolidado
FROM Agencia a
JOIN Conta c ON a.ID = c.Agencia_ID
GROUP BY a.Nome
ORDER BY Saldo_Total_Consolidado DESC;


SELECT 
    a.Nome AS Nome_Agencia,
    SUM(c.Saldo) AS Saldo_Total_Consolidado
FROM Agencia a
JOIN Conta c ON a.ID = c.Agencia_ID
GROUP BY a.Nome
HAVING SUM(c.Saldo) > 10000.00;


SELECT DISTINCT
    p.Nome
FROM Pessoa p
JOIN Cliente cl ON p.ID = cl.Pessoa_ID
JOIN Titularidade_Conta tc ON cl.Pessoa_ID = tc.Cliente_Pessoa_ID
JOIN Conta c ON tc.Conta_Numero = c.Numero
WHERE c.Saldo > (SELECT AVG(Saldo) FROM Conta);

SELECT
    t.Data,
    t.Tipo,
    t.Valor,
    t.Descricao,
    t.Conta_Origem_Numero,
    t.Conta_Destino_Numero
FROM Transacao t
JOIN Conta c ON t.Conta_Origem_Numero = c.Numero OR t.Conta_Destino_Numero = c.Numero
JOIN Titularidade_Conta tc ON c.Numero = tc.Conta_Numero
JOIN Pessoa p ON tc.Cliente_Pessoa_ID = p.ID
WHERE p.Nome = 'Ana Clara';

SELECT
    p.Nome, f.Cargo
    FROM Funcionario f
    JOIN Pessoa p ON f.Pessoa_ID = p.ID
    WHERE f.Pessoa_ID NOT IN (SELECT Gerente_ID FROM Agencia WHERE Gerente_ID IS NOT NULL);


SELECT p.Nome AS Funcionario, COUNT(*) AS Qtd_Atendimentos
FROM Funcionario_Atende_Cliente fac
JOIN Pessoa p ON fac.Funcionario_Pessoa_ID = p.ID
GROUP BY p.Nome
ORDER BY Qtd_Atendimentos DESC;

SELECT ag.Nome, COUNT(DISTINCT tc.Cliente_Pessoa_ID) AS Qtd_Clientes
FROM Agencia ag
JOIN Conta c ON ag.ID = c.Agencia_ID
JOIN Titularidade_Conta tc ON c.Numero = tc.Conta_Numero
GROUP BY ag.Nome
ORDER BY Qtd_Clientes DESC;

