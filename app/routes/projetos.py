from flask import Blueprint, flash, redirect, render_template, request, url_for

from app.domain.exceptions import BusinessRuleError, NotFoundError
from app.repositories.equipe_repository import EquipeRepository
from app.repositories.projeto_repository import ProjetoRepository
from app.services.equipe_service import EquipeService
from app.services.projeto_service import ProjetoService
from app.repositories.hackathon_repository import HackathonRepository
from app.repositories.participante_repository import ParticipanteRepository


projetos_bp = Blueprint(
    "projetos",
    __name__,
    url_prefix="/projetos",
)


equipe_repository = EquipeRepository()
projeto_repository = ProjetoRepository()

service = ProjetoService(
    equipe_repository,
    projeto_repository,
)

equipe_service = EquipeService(
    equipe_repository,
    HackathonRepository(),
    ParticipanteRepository(),
)


@projetos_bp.route("/novo", methods=["GET", "POST"])
def registrar():
    if request.method == "POST":
        equipe_id = int(request.form["equipe_id"])
        titulo = request.form["titulo"]
        descricao = request.form["descricao"]
        area_tematica = request.form["area_tematica"]

        try:
            service.registrar_projeto(
                equipe_id,
                titulo,
                descricao,
                area_tematica,
            )

            flash("Projeto registrado com sucesso.")

            return redirect(
                url_for("projetos.registrar")
            )

        except (BusinessRuleError, NotFoundError) as error:
            flash(str(error))

    equipes = equipe_service.listar_equipes()

    return render_template(
        "projetos/registrar.html",
        equipes=equipes,
    )