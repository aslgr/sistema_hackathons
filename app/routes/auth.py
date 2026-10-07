from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for

from app.domain.exceptions import BusinessRuleError
from app.repositories.usuario_repository import UsuarioRepository
from app.services.usuario_service import UsuarioService


auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

usuario_repository = UsuarioRepository()
usuario_service = UsuarioService(usuario_repository)


@auth_bp.before_app_request
def carregar_usuario_logado():
    usuario_id = session.get("usuario_id")

    if usuario_id is None:
        g.usuario = None
        return

    g.usuario = usuario_repository.buscar_por_id(usuario_id)
    if g.usuario is None:
        session.clear()


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if g.usuario is not None:
        return redirect(url_for("index"))

    if request.method == "POST":
        try:
            usuario = usuario_service.autenticar(
                request.form["email"],
                request.form["senha"],
            )
        except BusinessRuleError as error:
            flash(str(error))
        else:
            session.clear()
            session["usuario_id"] = usuario.id
            return redirect(url_for("index"))

    return render_template("auth/login.html")


@auth_bp.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    if g.usuario is not None:
        return redirect(url_for("index"))

    if request.method == "POST":
        try:
            usuario_service.cadastrar_participante(
                request.form["nome"],
                request.form["email"],
                request.form["senha"],
            )
        except BusinessRuleError as error:
            flash(str(error))
        else:
            flash("Cadastro realizado. Agora faça login.")
            return redirect(url_for("auth.login"))

    return render_template("auth/cadastro.html")


@auth_bp.post("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))
