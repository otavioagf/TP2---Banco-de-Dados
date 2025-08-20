-- CONSULTAS EXISTENTES --

-- Consulta 1: Listar todos os clientes e suas idades (Uso de VIEW).
-- Operadores: Projeção.
SELECT Nome, Idade FROM vw_cliente_idade ORDER BY Idade DESC;

-- Consulta 2: Listar todas as agências e o nome de seus respectivos gerentes.
-- Operadores: Junção Externa (LEFT JOIN), Projeção.
SELECT 
    a.Nome AS Nome_Agencia,
    p.Nome AS Nome_Gerente
FROM Agencia a
LEFT JOIN Funcionario f ON a.Gerente_ID = f.Pessoa_ID
LEFT JOIN Pessoa p ON f.Pessoa_ID = p.ID;

-- Consulta 3: Listar clientes com saldo em conta superior a 5000.
-- Operadores: Seleção, Junção, Projeção.
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

-- Consulta 4 (AGREGAÇÃO): Contar quantos funcionários cada agência possui.
-- Operadores: Agregação (COUNT), Agrupamento (GROUP BY), Junção.
SELECT 
    a.Nome AS Nome_Agencia,
    COUNT(f.Pessoa_ID) AS Quantidade_Funcionarios
FROM Agencia a
JOIN Funcionario f ON a.ID = f.Agencia_ID
GROUP BY a.Nome
ORDER BY Quantidade_Funcionarios DESC;

-- Consulta 5 (AGREGAÇÃO): Calcular o saldo total (soma de todos os saldos) por agência.
-- Operadores: Agregação (SUM), Agrupamento (GROUP BY), Junção.
SELECT 
    a.Nome AS Nome_Agencia,
    SUM(c.Saldo) AS Saldo_Total_Consolidado
FROM Agencia a
JOIN Conta c ON a.ID = c.Agencia_ID
GROUP BY a.Nome
ORDER BY Saldo_Total_Consolidado DESC;

-- Consulta 6 (AGREGAÇÃO com HAVING): Listar agências que possuem mais de R$ 10.000,00 em saldo consolidado.
-- Operadores: Agregação (SUM), Agrupamento (GROUP BY), Seleção sobre grupo (HAVING).
SELECT 
    a.Nome AS Nome_Agencia,
    SUM(c.Saldo) AS Saldo_Total_Consolidado
FROM Agencia a
JOIN Conta c ON a.ID = c.Agencia_ID
GROUP BY a.Nome
HAVING SUM(c.Saldo) > 10000.00;

-- Consulta 7 (SUBQUERY): Listar os nomes dos clientes que possuem contas com saldo acima da média de todos os saldos.
-- Operadores: Projeção, Junção, Subconsulta na cláusula WHERE.
SELECT DISTINCT
    p.Nome
FROM Pessoa p
JOIN Cliente cl ON p.ID = cl.Pessoa_ID
JOIN Titularidade_Conta tc ON cl.Pessoa_ID = tc.Cliente_Pessoa_ID
JOIN Conta c ON tc.Conta_Numero = c.Numero
WHERE c.Saldo > (SELECT AVG(Saldo) FROM Conta);

-- Consulta 8: Listar todas as transações (saques, depósitos e transferências) da cliente 'Ana Clara'.
-- Operadores: Múltiplas Junções, Seleção.
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

-- Consulta 9: Listar pessoas que são clientes e funcionários ao mesmo tempo.
-- Operadores: Junção, Interseção (implícita pelo JOIN em chaves iguais).
SELECT
    p.Nome,
    p.CPF,
    f.Matricula,
    f.Cargo
FROM Pessoa p
JOIN Cliente c ON p.ID = c.Pessoa_ID
JOIN Funcionario f ON p.ID = f.Pessoa_ID;