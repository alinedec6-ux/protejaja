import os
import sqlite3

from werkzeug.security import generate_password_hash

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DB_PATH = os.path.join(BASE_DIR, "db", "app.db")
UPLOAD_DIR = os.path.join(BASE_DIR, "backend", "uploads")

ADMIN_EMAIL = "admin@protejaja.com"
ADMIN_SENHA = "admin123"

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
    denunciado TEXT NOT NULL DEFAULT '',
    assunto TEXT NOT NULL DEFAULT 'Sem assunto',
    categoria TEXT NOT NULL DEFAULT 'Geral',
    descricao TEXT NOT NULL,
    anexo TEXT,
    status TEXT NOT NULL DEFAULT 'pendente',
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

    colunas_reports = {
        r[1] for r in conn.execute("PRAGMA table_info(reports)").fetchall()
    }
    if "assunto" not in colunas_reports:
        conn.execute("ALTER TABLE reports ADD COLUMN assunto TEXT NOT NULL DEFAULT 'Sem assunto'")
    if "denunciado" not in colunas_reports:
        conn.execute("ALTER TABLE reports ADD COLUMN denunciado TEXT NOT NULL DEFAULT ''")
    if "status" not in colunas_reports:
        conn.execute("ALTER TABLE reports ADD COLUMN status TEXT NOT NULL DEFAULT 'pendente'")

    colunas_users = {
        r[1] for r in conn.execute("PRAGMA table_info(users)").fetchall()
    }
    if "is_admin" not in colunas_users:
        conn.execute("ALTER TABLE users ADD COLUMN is_admin INTEGER NOT NULL DEFAULT 0")

    admin = conn.execute(
        "SELECT id FROM users WHERE email = ? COLLATE NOCASE", (ADMIN_EMAIL,)
    ).fetchone()
    if admin is None:
        conn.execute(
            "INSERT INTO users (nome, email, data_nascimento, cidade, endereco, senha_hash, is_admin) "
            "VALUES (?, ?, ?, ?, ?, ?, 1)",
            (
                "Administrador",
                ADMIN_EMAIL,
                "01/01/2000",
                "Matão",
                "Central",
                generate_password_hash(ADMIN_SENHA),
            ),
        )
    else:
        conn.execute("UPDATE users SET is_admin = 1 WHERE email = ? COLLATE NOCASE", (ADMIN_EMAIL,))

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
        "SELECT id, nome, email, data_nascimento, cidade, endereco, senha_hash, criado_em, is_admin "
        "FROM users WHERE email = ? COLLATE NOCASE",
        (email,),
    ).fetchone()
    conn.close()
    return row


def usuario_por_id(user_id):
    conn = get_connection()
    row = conn.execute(
        "SELECT id, nome, email, data_nascimento, cidade, endereco, senha_hash, criado_em, is_admin "
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


def criar_denuncia(user_id, denunciado, assunto, categoria, descricao, anexo):
    conn = get_connection()
    cur = conn.execute(
        "INSERT INTO reports (user_id, denunciado, assunto, categoria, descricao, anexo) "
        "VALUES (?, ?, ?, ?, ?, ?)",
        (user_id, denunciado, assunto, categoria, descricao, anexo),
    )
    conn.commit()
    report_id = cur.lastrowid
    conn.close()
    return report_id


def denuncia_do_usuario(user_id, denuncia_id):
    conn = get_connection()
    row = conn.execute(
        "SELECT id, denunciado, assunto, categoria, descricao, anexo, criado_em "
        "FROM reports WHERE id = ? AND user_id = ?",
        (denuncia_id, user_id),
    ).fetchone()
    conn.close()
    return row


def denuncias_do_usuario(user_id):
    conn = get_connection()
    rows = conn.execute(
        "SELECT id, denunciado, assunto, categoria, descricao, anexo, criado_em "
        "FROM reports WHERE user_id = ? ORDER BY id DESC",
        (user_id,),
    ).fetchall()
    conn.close()
    return rows


def anexos_do_usuario(user_id):
    conn = get_connection()
    rows = conn.execute(
        "SELECT anexo FROM reports WHERE user_id = ? AND anexo IS NOT NULL",
        (user_id,),
    ).fetchall()
    conn.close()
    return rows


def apagar_conta_completa(user_id):
    conn = get_connection()
    conn.execute("DELETE FROM reports WHERE user_id = ?", (user_id,))
    conn.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()


def promover_admin(user_id):
    conn = get_connection()
    conn.execute("UPDATE users SET is_admin = 1 WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()


def usuario_eh_admin(user_id):
    conn = get_connection()
    row = conn.execute("SELECT is_admin FROM users WHERE id = ?", (user_id,)).fetchone()
    conn.close()
    return bool(row and row["is_admin"])


def todas_denuncias():
    conn = get_connection()
    rows = conn.execute(
        "SELECT id, user_id, denunciado, assunto, categoria, descricao, anexo, status, criado_em "
        "FROM reports ORDER BY id DESC",
    ).fetchall()
    conn.close()
    return rows


def atualizar_status_denuncia(denuncia_id, novo_status):
    conn = get_connection()
    conn.execute("UPDATE reports SET status = ? WHERE id = ?", (novo_status, denuncia_id))
    conn.commit()
    conn.close()


def denuncias_aprovadas():
    conn = get_connection()
    rows = conn.execute(
        "SELECT id, denunciado, assunto, categoria, descricao, anexo, criado_em "
        "FROM reports WHERE status = 'aprovada' ORDER BY id DESC",
    ).fetchall()
    conn.close()
    return rows