# 💰 BankInfo - Sistema Bancário em PostgreSQL

Este repositório contém a implementação completa de um banco de dados relacional no PostgreSQL, desenvolvido como parte do **Trabalho Prático 2 (TP2)** da disciplina **Banco de Dados I** – Universidade Federal de Ouro Preto (UFOP).

## 👨‍🏫 Professor
Marcos Emiliano

## 👥 Integrantes do grupo
- Otávio Augusto Guimarães Ferreira  
- Matheus Martins Nunes  
- Victor Emanuel Mourão de Castro  
- Vitor Pureza Cabral  
- Vinícius Andrade Costa

---

## 📚 Descrição do Projeto

O projeto visa implementar fisicamente um banco de dados baseado em um modelo conceitual ERE definido no Trabalho Prático 1 (TP1). A aplicação simula operações de um sistema bancário, com suporte para:

- Clientes e Funcionários (generalização via tabela Pessoa)
- Contas bancárias e múltiplos titulares
- Agências com gerentes
- Cartões de débito/crédito (entidade fraca)
- Transações com origem e destino
- Relacionamento N:N entre funcionários e clientes (atendimentos)

---

## 📁 Estrutura do repositório
📦 TP2 - Banco de Dados
├── sql/
│ ├── esquema_fisico.sql # Comandos DDL para criação do banco
│ ├── inserts_teste.sql # Dados fictícios para testes
│ └── consultas_algebra.sql # Consultas SQL com operadores da álgebra relacional
├── documento/
│ └── tp2_modelo_abnt.docx # Documento do trabalho no padrão ABNT
├── apresentacao/
│ └── slides_apresentacao.pptx # Slides para apresentação final
└── README.md # Descrição geral do projeto

---

## 🛠️ Tecnologias Utilizadas

- PostgreSQL 15+
- SQL (DDL + DML + Queries com Álgebra Relacional)
- pgAdmin 4
- Git & GitHub

---

## 📌 Entregáveis

- [x] Modelo Relacional baseado no ERE corrigido
- [x] Esquema físico implementado em PostgreSQL
- [x] Consultas SQL utilizando operadores da álgebra relacional (`SELECT`, `JOIN`, `GROUP BY`, `HAVING`, etc.)
- [x] Documento do projeto em ABNT
- [x] Slides de apresentação

---

## ✅ Como executar

1. Clone o repositório:
```bash
git clone https://github.com/otavioagf/TP2---Banco-de-Dados.git

