# database.py - VERSÃO FINAL E REVISADA
import sqlite3

# Conecta ao banco de dados (cria o arquivo se não existir)
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# --- Tabela de Usuários ---
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL
);
""")

# --- Tabela de Livros ---
cursor.execute("""
CREATE TABLE IF NOT EXISTS books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    description TEXT,
    cover_image TEXT,
    available BOOLEAN NOT NULL DEFAULT 1,
    category TEXT,
    owner_id INTEGER NOT NULL,
    FOREIGN KEY (owner_id) REFERENCES users (id) ON DELETE CASCADE
);
""")

# --- Tabela de Empréstimos ---
cursor.execute("""
CREATE TABLE IF NOT EXISTS loans (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    book_id INTEGER NOT NULL,
    requester_id INTEGER NOT NULL,
    owner_id INTEGER NOT NULL,
    status TEXT NOT NULL, -- 'pending', 'approved', 'denied', 'returned'
    request_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    decision_date DATETIME,
    return_date DATETIME,
    start_date TEXT, 
    end_date TEXT,
    requester_seen BOOLEAN NOT NULL DEFAULT 1, -- 1 (true) se o solicitante viu, 0 (false) se for uma notificação nova.
    FOREIGN KEY (book_id) REFERENCES books (id) ON DELETE CASCADE,
    FOREIGN KEY (requester_id) REFERENCES users (id),
    FOREIGN KEY (owner_id) REFERENCES users (id)
);
""")

# Salva as alterações e fecha a conexão
conn.commit()
conn.close()

print("Banco de dados 'database.db' com estrutura final criado com sucesso!")
