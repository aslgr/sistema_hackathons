from flask import Blueprint, flash, g, redirect, render_template, request, url_for

from app.auth.decorators import role_required
from app.domain.exceptions import BusinessRuleError, NotFoundError
from app.domain.models import PapelUsuario
from app.repositories.equipe_repository import EquipeRepository
from app.repositories.hackathon_repository import HackathonRepository
from app.repositories.projeto_repository import ProjetoRepository
from app.repositories.usuario_repository import UsuarioRepository
from app.services.hackathon_service import HackathonService
from app.services.projeto_service import ProjetoService


projetos_bp = Blueprint("projetos", __name__, url_prefix="/projetos")

equipe_repository = EquipeRepository()
projeto_repository = ProjetoRepository()
hackathon_repository = HackathonRepository()
usuario_repository = UsuarioRepository()

projeto_service = ProjetoService(
    equipe_repository,
    projeto_repository,
    hackathon_repository,
)
hackathon_service = HackathonService(hackathon_repository, usuario_repository)


@projetos_bp.route("/novo", methods=["GET", "POST"])
@role_required(PapelUsuario.PARTICIPANTE)
def registrar():
    if request.method == "POST":
        try:
            projeto_service.registrar_projeto(
                equipe_id=int(request.form["equipe_id"]),
                titulo=request.form["titulo"],
                descricao=request.form["descricao"],
                area_tematica=request.form["area_tematica"],
                solicitante_id=g.usuario.id,
            )
        except ValueError:
            flash("Selecione uma equipe válida.")
        except (BusinessRuleError, NotFoundError) as error:
            flash(str(error))
        else:
            flash("Projeto registrado com sucesso.")
            return redirect(url_for("projetos.registrar"))

    return render_template(
        "projetos/registrar.html",
        equipes=equipe_repository.listar_por_lider(g.usuario.id),
    )


@projetos_bp.get("/")
def consultar():
    hackathon_id = request.args.get("hackathon_id", type=int)
    projetos = []

    if hackathon_id is not None:
        try:
            projetos = projeto_service.consultar_projetos(hackathon_id)
        except NotFoundError as error:
            flash(str(error))

    return render_template(
        "projetos/consultar.html",
        hackathons=hackathon_service.listar_hackathons(),
        projetos=projetos,
        hackathon_id=hackathon_id,
    )
