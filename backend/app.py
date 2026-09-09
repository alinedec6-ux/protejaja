import os
import re
import secrets
from functools import wraps

from flask import (
    Flask,
    abort,
    flash,
    redirect,
    render_template,
    request,
    send_from_directory,
    session,
    url_for,
)
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename

import database as db
from profanity import contem_ofensa, sanitizar

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
HOME_DIR = os.path.join(BASE_DIR, "home")
TEMPLATE_DIR = os.path.join(BASE_DIR, "backend", "templates")
UPLOAD_DIR = db.UPLOAD_DIR

EXTENSOES_PERMITIDAS = {"png", "jpg", "jpeg", "gif", "webp", "heic", "heif", "pdf", "mp4", "mov"}
MAX_ANEXO = 5 * 1024 * 1024


def arquivo_permitido(nome):
    return "." in nome and nome.rsplit(".", 1)[1].lower() in EXTENSOES_PERMITIDAS


def login_obrigatorio(visao):
    @wraps(visao)
    def envolvida(*args, **kwargs):
        if "user_id" not in session:
            flash("Faça login para acessar essa página.", "error")
            return redirect(url_for("login"))
        return visao(*args, **kwargs)

    return envolvida


def validar_email(email):
    return re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email) is not None


def usuario_atual():
    user_id = session.get("user_id")
    if not user_id:
        return None
    return db.usuario_por_id(user_id)


def create_app():
    app = Flask(__name__, template_folder=TEMPLATE_DIR)
    app.config["DATABASE"] = db.DB_PATH
    app.config["MAX_CONTENT_LENGTH"] = MAX_ANEXO
    app.secret_key = os.environ.get("SECRET_KEY", "protejaja-chave-desenvolvimento")

    app.teardown_appcontext(db.close_connection)

    with app.app_context():
        db.init_db()

    @app.context_processor
    def injetar_contexto():
        return {"user": usuario_atual()}

    @app.route("/")
    def index():
        return redirect(url_for("home"))

    @app.route("/home")
    def home():
        return render_template("home.html")

    @app.route("/home/<path:filename>")
    def home_static(filename):
        return send_from_directory(HOME_DIR, filename)

    @app.route("/uploads/<path:filename>")
    def uploads(filename):
        return send_from_directory(UPLOAD_DIR, filename)

    @app.route("/cadastro", methods=["GET", "POST"])
    def cadastro():
        if request.method == "POST":
            nome = (request.form.get("nome") or "").strip()
            email = (request.form.get("email") or "").strip().lower()
            data_nascimento = (request.form.get("data_nascimento") or "").strip()
            cidade = (request.form.get("cidade") or "").strip()
            endereco = (request.form.get("endereco") or "").strip()
            senha = request.form.get("senha") or ""

            if not all([nome, email, data_nascimento, cidade, endereco, senha]):
                flash("Preencha todos os campos do cadastro.", "error")
            elif not validar_email(email):
                flash("Informe um e-mail válido.", "error")
            elif len(senha) < 6:
                flash("A senha deve ter no mínimo 6 caracteres.", "error")
            elif contem_ofensa(nome):
                flash("O nome contém palavras ofensivas e não pode ser usado.", "error")
            elif contem_ofensa(cidade) or contem_ofensa(endereco):
                flash("Cidade ou endereço contêm palavras ofensivas.", "error")
            elif db.email_cadastrado(email):
                flash("Já existe uma conta com esse e-mail.", "error")
            else:
                senha_hash = generate_password_hash(senha)
                db.criar_usuario(
                    nome.strip(),
                    email,
                    data_nascimento,
                    cidade,
                    endereco,
                    senha_hash,
                )
                flash("Conta criada com sucesso! Faça login para continuar.", "success")
                return redirect(url_for("login"))

        return render_template("cadastro.html")

    @app.route("/login", methods=["GET", "POST"])
    def login():
        if request.method == "POST":
            email = (request.form.get("email") or "").strip().lower()
            senha = request.form.get("senha") or ""

            usuario = db.usuario_por_email(email) if email else None

            if usuario and check_password_hash(usuario["senha_hash"], senha):
                session.clear()
                session["user_id"] = usuario["id"]
                flash(f"Bem-vindo(a), {usuario['nome']}!", "success")
                return redirect(url_for("home"))

            flash("E-mail ou senha incorretos.", "error")

        return render_template("login.html")

    @app.route("/logout")
    def logout():
        session.clear()
        flash("Você saiu da sua conta.", "success")
        return redirect(url_for("home"))

    @app.route("/recuperar", methods=["GET", "POST"])
    def recuperar():
        resultado = None

        if request.method == "POST":
            email = (request.form.get("email") or "").strip().lower()
            data_nascimento = (request.form.get("data_nascimento") or "").strip()

            usuario = db.usuario_por_email(email) if email else None

            if not usuario or usuario["data_nascimento"] != data_nascimento:
                flash("Dados não conferem com nenhuma conta cadastrada.", "error")
            else:
                temporaria = secrets.token_urlsafe(8)
                db.atualizar_senha(usuario["id"], generate_password_hash(temporaria))
                resultado = (usuario["nome"], temporaria)

        return render_template("recuperar.html", senha_temporaria=resultado)

    @app.route("/denuncias", methods=["GET", "POST"])
    @login_obrigatorio
    def denuncias():
        usuario = db.usuario_por_id(session["user_id"])

        if request.method == "POST":
            denunciado = (request.form.get("denunciado") or "").strip()
            assunto = (request.form.get("assunto") or "").strip()
            categoria = (request.form.get("categoria") or "Geral").strip()
            descricao = (request.form.get("descricao") or "").strip()
            anexo = request.files.get("anexo")
            nome_anexo = None

            if not denunciado:
                flash("Informe quem você está denunciando.", "error")
            elif not assunto:
                flash("Informe sobre o que você está denunciando.", "error")
            elif not descricao:
                flash("Descreva a denúncia antes de enviar.", "error")
            elif contem_ofensa(denunciado):
                flash("O nome do denunciado contém palavras ofensivas.", "error")
            elif contem_ofensa(assunto):
                flash("O assunto contém palavras ofensivas.", "error")
            elif contem_ofensa(descricao):
                flash("A denúncia contém palavras ofensivas e não foi enviada.", "error")
            else:
                nome_anexo = None
                anexo_invalido = False

                if anexo and anexo.filename:
                    nome_seguro = secure_filename(anexo.filename)
                    if not arquivo_permitido(anexo.filename) or not nome_seguro:
                        anexo_invalido = True
                        flash("Tipo de anexo não permitido (use imagem, PDF ou vídeo).", "error")
                    else:
                        nome_anexo = nome_seguro
                        anexo.save(os.path.join(UPLOAD_DIR, nome_seguro))

                if not anexo_invalido:
                    db.criar_denuncia(
                        usuario["id"],
                        sanitizar(denunciado),
                        sanitizar(assunto),
                        categoria,
                        sanitizar(descricao),
                        nome_anexo,
                    )
                    flash("Denúncia enviada com sucesso!", "success")

        denuncias = db.denuncias_do_usuario(usuario["id"])
        return render_template("denuncias.html", denuncias=denuncias)

    return app