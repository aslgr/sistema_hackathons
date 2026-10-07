from flask import Blueprint, flash, g, redirect, render_template, request, url_for

from app.auth.decorators import role_required
from app.domain.exceptions import BusinessRuleError, NotFoundError
from app.domain.models import PapelUsuario
from app.repositories.equipe_repository import EquipeRepository
from app.repositories.hackathon_repository import HackathonRepository
from app.repositories.usuario_repository import UsuarioRepository
from app.services.equipe_service import EquipeService
from app.services.hackathon_service import HackathonService


equipes_bp = Blueprint("equipes", __name__, url_prefix="/equipes")

equipe_repository = EquipeRepository()
hackathon_repository = HackathonRepository()
usuario_repository = UsuarioRepository()

equipe_service = EquipeService(
    equipe_repository,
    hackathon_repository,
    usuario_repository,
)
hackathon_service = HackathonService(hackathon_repository, usuario_repository)


@equipes_bp.route("/nova", methods=["GET", "POST"])
@role_required(PapelUsuario.PARTICIPANTE)
def criar():
    if request.method == "POST":
        try:
            equipe_service.criar_equipe(
                hackathon_id=int(request.form["hackathon_id"]),
                nome=request.form["nome"],
                lider_id=g.usuario.id,
            )
        except ValueError:
            flash("Selecione um hackathon válido.")
        except (BusinessRuleError, NotFoundError) as error:
            flash(str(error))
        else:
            flash("Equipe criada com sucesso. Você é o líder.")
            return redirect(url_for("equipes.criar"))

    return render_template(
        "equipes/criar.html",
        hackathons=hackathon_service.listar_hackathons(),
    )


@equipes_bp.route("/adicionar-participante", methods=["GET", "POST"])
@role_required(PapelUsuario.PARTICIPANTE)
def adicionar_participante():
    if request.method == "POST":
        try:
            equipe_service.adicionar_participante(
                equipe_id=int(request.form["equipe_id"]),
                participante_id=int(request.form["participante_id"]),
                solicitante_id=g.usuario.id,
            )
        except ValueError:
            flash("Selecione uma equipe e um participante válidos.")
        except (BusinessRuleError, NotFoundError) as error:
            flash(str(error))
        else:
            flash("Participante adicionado com sucesso.")
            return redirect(url_for("equipes.adicionar_participante"))

    return render_template(
        "equipes/adicionar_participante.html",
        equipes=equipe_service.listar_equipes_do_lider(g.usuario.id),
        participantes=usuario_repository.listar_por_papel(PapelUsuario.PARTICIPANTE),
    )


@equipes_bp.get("/")
def consultar():
    hackathon_id = request.args.get("hackathon_id", type=int)
    equipes = []

    if hackathon_id is not None:
        try:
            equipes = equipe_service.consultar_equipes(hackathon_id)
        except NotFoundError as error:
            flash(str(error))

    return render_template(
        "equipes/consultar.html",
        hackathons=hackathon_service.listar_hackathons(),
        equipes=equipes,
        hackathon_id=hackathon_id,
    )
