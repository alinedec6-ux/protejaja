import os
import sqlite3

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DB_PATH = os.path.join(BASE_DIR, "db", "app.db")
UPLOAD_DIR = os.path.join(BASE_DIR, "backend", "uploads")

SCHEMA = """
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    data_nascimento TEXT NOT NULL,
    cidade TEXT NOT NULL,
    endereco TEXT NOT NULL,
    senha_hash TEXT NOT NULL,
    criado_em TEXT NOT NULL DEFAULT (datetime('now', 'localtime'))
);

CREATE TABLE IF NOT EXISTS reports (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    categoria TEXT NOT NULL DEFAULT 'Geral',
    descricao TEXT NOT NULL,
    anexo TEXT,
    criado_em TEXT NOT NULL DEFAULT (datetime('now', 'localtime')),
    FOREIGN KEY (user_id) REFERENCES users (id)
);
"""


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    conn = get_connection()
    conn.executescript(SCHEMA)
    conn.commit()
    conn.close()


def close_connection(exception=None):
    pass


def email_cadastrado(email):
    conn = get_connection()
    row = conn.execute("SELECT id FROM users WHERE email = ? COLLATE NOCASE", (email,)).fetchone()
    conn.close()
    return row is not None


def criar_usuario(nome, email, data_nascimento, cidade, endereco, senha_hash):
    conn = get_connection()
    cur = conn.execute(
        "INSERT INTO users (nome, email, data_nascimento, cidade, endereco, senha_hash) "
        "VALUES (?, ?, ?, ?, ?, ?)",
        (nome, email, data_nascimento, cidade, endereco, senha_hash),
    )
    conn.commit()
    user_id = cur.lastrowid
    conn.close()
    return user_id


def usuario_por_email(email):
    conn = get_connection()
    row = conn.execute(
        "SELECT id, nome, email, data_nascimento, cidade, endereco, senha_hash, criado_em "
        "FROM users WHERE email = ? COLLATE NOCASE",
        (email,),
    ).fetchone()
    conn.close()
    return row


def usuario_por_id(user_id):
    conn = get_connection()
    row = conn.execute(
        "SELECT id, nome, email, data_nascimento, cidade, endereco, senha_hash, criado_em "
        "FROM users WHERE id = ?",
        (user_id,),
    ).fetchone()
    conn.close()
    return row


def atualizar_senha(user_id, senha_hash):
    conn = get_connection()
    conn.execute("UPDATE users SET senha_hash = ? WHERE id = ?", (senha_hash, user_id))
    conn.commit()
    conn.close()


def criar_denuncia(user_id, categoria, descricao, anexo):
    conn = get_connection()
    cur = conn.execute(
        "INSERT INTO reports (user_id, categoria, descricao, anexo) VALUES (?, ?, ?, ?)",
        (user_id, categoria, descricao, anexo),
    )
    conn.commit()
    report_id = cur.lastrowid
    conn.close()
    return report_id


def denuncias_do_usuario(user_id):
    conn = get_connection()
    rows = conn.execute(
        "SELECT id, categoria, descricao, anexo, criado_em "
        "FROM reports WHERE user_id = ? ORDER BY id DESC",
        (user_id,),
    ).fetchall()
    conn.close()
    return rows