from flask import Blueprint, flash, g, redirect, render_template, request, url_for

from app.auth.decorators import role_required
from app.domain.exceptions import BusinessRuleError, NotFoundError
from app.domain.models import PapelUsuario
from app.repositories.hackathon_repository import HackathonRepository
from app.repositories.usuario_repository import UsuarioRepository
from app.services.hackathon_service import HackathonService
from app.services.usuario_service import UsuarioService


usuarios_bp = Blueprint("usuarios", __name__, url_prefix="/usuarios")

usuario_repository = UsuarioRepository()
hackathon_repository = HackathonRepository()
usuario_service = UsuarioService(usuario_repository)
hackathon_service = HackathonService(hackathon_repository, usuario_repository)


@usuarios_bp.route("/novo-colaborador", methods=["GET", "POST"])
@role_required(PapelUsuario.ORGANIZADOR)
def cadastrar_colaborador():
    if request.method == "POST":
        try:
            usuario_service.cadastrar_colaborador(
                nome=request.form["nome"],
                email=request.form["email"],
                senha=request.form["senha"],
                papel=request.form["papel"],
            )
        except BusinessRuleError as error:
            flash(str(error))
        else:
            flash("Colaborador cadastrado com sucesso.")
            return redirect(url_for("usuarios.cadastrar_colaborador"))

    return render_template(
        "usuarios/cadastrar_colaborador.html",
        colaboradores=usuario_service.listar_colaboradores(),
    )


@usuarios_bp.route("/associar", methods=["GET", "POST"])
@role_required(PapelUsuario.ORGANIZADOR)
def associar():
    if request.method == "POST":
        try:
            usuario_id = int(request.form["usuario_id"])
            hackathon_id = int(request.form["hackathon_id"])
            usuario = usuario_repository.buscar_por_id(usuario_id)

            if usuario is None:
                raise NotFoundError("Usuário não encontrado.")

            if usuario.papel == PapelUsuario.JURADO:
                hackathon_service.associar_jurado(
                    hackathon_id,
                    usuario_id,
                    g.usuario.id,
                )
            elif usuario.papel == PapelUsuario.MENTOR:
                hackathon_service.associar_mentor(
                    hackathon_id,
                    usuario_id,
                    g.usuario.id,
                )
            else:
                raise BusinessRuleError(
                    "Este usuário não pode ser associado como colaborador."
                )
        except ValueError:
            flash("Selecione um colaborador e um hackathon válidos.")
        except (BusinessRuleError, NotFoundError) as error:
            flash(str(error))
        else:
            flash("Colaborador associado com sucesso.")
            return redirect(url_for("usuarios.associar"))

    return render_template(
        "usuarios/associar.html",
        hackathons=hackathon_service.listar_por_organizador(g.usuario.id),
        colaboradores=usuario_service.listar_colaboradores(),
    )
