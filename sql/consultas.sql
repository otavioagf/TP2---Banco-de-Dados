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
