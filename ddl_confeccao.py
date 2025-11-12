import sqlite3

# =======================================================
# CONEXÃO E CRIAÇÃO DO BANCO
# =======================================================
conn = sqlite3.connect("confeccao.db")
cursor = conn.cursor()

# Ativa o uso de chaves estrangeiras no SQLite
cursor.execute("PRAGMA foreign_keys = ON;")

# =======================================================
# CRIAÇÃO DAS TABELAS
# =======================================================

# Tabela: PESSOA (classe base)
cursor.execute("""
CREATE TABLE IF NOT EXISTS pessoa (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    telefone TEXT,
    email TEXT,
    tipo TEXT CHECK (tipo IN ('Cliente', 'Funcionario')) NOT NULL
);
""")

# Tabela: CLIENTE (herda de Pessoa)
cursor.execute("""
CREATE TABLE IF NOT EXISTS cliente (
    id INTEGER PRIMARY KEY,
    cpf TEXT UNIQUE,
    endereco TEXT,
    FOREIGN KEY (id) REFERENCES pessoa(id) ON DELETE CASCADE
);
""")

# Tabela: FUNCIONARIO (herda de Pessoa)
cursor.execute("""
CREATE TABLE IF NOT EXISTS funcionario (
    id INTEGER PRIMARY KEY,
    matricula TEXT UNIQUE,
    cargo TEXT,
    salario REAL DEFAULT 0.0,
    FOREIGN KEY (id) REFERENCES pessoa(id) ON DELETE CASCADE
);
""")

# Tabela: ROUPA
cursor.execute("""
CREATE TABLE IF NOT EXISTS roupa (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    codigo TEXT UNIQUE NOT NULL,
    descricao TEXT NOT NULL,
    tamanho TEXT,
    cor TEXT,
    preco REAL NOT NULL CHECK (preco >= 0),
    estoque INTEGER NOT NULL DEFAULT 0 CHECK (estoque >= 0)
);
""")

# Tabela: PEDIDO
cursor.execute("""
CREATE TABLE IF NOT EXISTS pedido (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    numero TEXT UNIQUE NOT NULL,
    cliente_id INTEGER NOT NULL,
    data_pedido TEXT DEFAULT (datetime('now')),
    status TEXT CHECK (status IN ('Aberto', 'Em processamento', 'Finalizado', 'Cancelado')) DEFAULT 'Aberto',
    FOREIGN KEY (cliente_id) REFERENCES cliente(id)
);
""")

# Tabela: ITEM_PEDIDO
cursor.execute("""
CREATE TABLE IF NOT EXISTS item_pedido (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    pedido_id INTEGER NOT NULL,
    roupa_id INTEGER NOT NULL,
    quantidade INTEGER NOT NULL CHECK (quantidade > 0),
    valor_unitario REAL NOT NULL CHECK (valor_unitario >= 0),
    FOREIGN KEY (pedido_id) REFERENCES pedido(id) ON DELETE CASCADE,
    FOREIGN KEY (roupa_id) REFERENCES roupa(id)
);
""")

# Tabela: PAGAMENTO
cursor.execute("""
CREATE TABLE IF NOT EXISTS pagamento (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    pedido_id INTEGER NOT NULL UNIQUE,
    valor REAL NOT NULL CHECK (valor >= 0),
    forma TEXT CHECK (forma IN ('Dinheiro', 'Cartão', 'Pix', 'Boleto')) NOT NULL,
    status TEXT CHECK (status IN ('Pendente', 'Processando', 'Confirmado', 'Estornado')) DEFAULT 'Pendente',
    data_pagamento TEXT DEFAULT (datetime('now')),
    FOREIGN KEY (pedido_id) REFERENCES pedido(id) ON DELETE CASCADE
);
""")

# Tabela: PRODUCAO
cursor.execute("""
CREATE TABLE IF NOT EXISTS producao (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    data_inicio TEXT,
    data_fim TEXT,
    status TEXT CHECK (status IN ('Planejada', 'Em andamento', 'Concluída', 'Cancelada')) DEFAULT 'Planejada'
);
""")

# Tabela: ETAPA_PRODUCAO
cursor.execute("""
CREATE TABLE IF NOT EXISTS etapa_producao (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tipo TEXT CHECK (tipo IN ('Corte', 'Costura', 'Bordado', 'Acabamento', 'Inspeção')) NOT NULL,
    descricao TEXT,
    ordem INTEGER NOT NULL
);
""")

# Tabela: EXECUCAO_ETAPA
cursor.execute("""
CREATE TABLE IF NOT EXISTS execucao_etapa (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    papel TEXT NOT NULL,
    funcionario_id INTEGER,
    horas_trabalhadas REAL DEFAULT 0.0,
    observacoes TEXT,
    FOREIGN KEY (funcionario_id) REFERENCES funcionario(id)
);
""")

# =======================================================
# FINALIZAÇÃO
# =======================================================
conn.commit()
conn.close()

print("✅ Banco de dados 'confeccao.db' criado com sucesso!")
print("📊 Tabelas criadas: pessoa, cliente, funcionario, roupa, pedido, item_pedido, pagamento, producao, etapa_producao, execucao_etapa")
