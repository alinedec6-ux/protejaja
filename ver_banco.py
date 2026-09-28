"""
Script utilitário para inspecionar os dados do banco SQLite (db/app.db).
Execute: python ver_banco.py
"""
import os
import sqlite3
import sys

# Garante compatibilidade de caracteres no terminal Windows
if sys.stdout.encoding != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

DB_PATH = os.path.join(os.path.dirname(__file__), "db", "app.db")


def inspecionar():
    if not os.path.exists(DB_PATH):
        print(f"[ERRO] Banco de dados nao encontrado em: {DB_PATH}")
        return

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    print("=" * 75)
    print("USUARIOS CADASTRADOS NA TABELA 'users'")
    print("=" * 75)
    users = conn.execute(
        "SELECT id, nome, email, data_nascimento, cidade, is_admin, criado_em FROM users"
    ).fetchall()

    if not users:
        print("Nenhum usuario cadastrado.")
    else:
        for u in users:
            tipo = "ADMIN" if u["is_admin"] else "CIDADAO"
            print(
                f"[{tipo:<7}] ID: {u['id']:<2} | {u['nome']:<20} | {u['email']:<30} | {u['cidade']:<15} | Nasc: {u['data_nascimento']}"
            )

    print("\n" + "=" * 75)
    print("ULTIMAS DENUNCIAS NA TABELA 'reports'")
    print("=" * 75)
    reports = conn.execute(
        "SELECT id, user_id, denunciado, assunto, categoria, status, criado_em FROM reports ORDER BY id DESC LIMIT 10"
    ).fetchall()

    if not reports:
        print("Nenhuma denuncia registrada.")
    else:
        for r in reports:
            print(
                f"#{r['id']:<3} | Status: {r['status']:<22} | Cat: {r['categoria']:<12} | Alvo: {r['denunciado']:<22} | Assunto: {r['assunto']}"
            )

    total_denuncias = conn.execute("SELECT COUNT(*) FROM reports").fetchone()[0]
    print(f"\nTotal geral: {len(users)} usuario(s) | {total_denuncias} denuncia(s) no banco.")
    print("=" * 75)


if __name__ == "__main__":
    inspecionar()
