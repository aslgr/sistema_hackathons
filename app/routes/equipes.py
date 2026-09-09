from flask import Blueprint, flash, redirect, render_template, request, url_for

from app.domain.exceptions import BusinessRuleError, NotFoundError
from app.repositories.equipe_repository import EquipeRepository
from app.repositories.hackathon_repository import HackathonRepository
from app.repositories.participante_repository import ParticipanteRepository
from app.services.equipe_service import EquipeService
from app.services.hackathon_service import HackathonService
from app.services.participante_service import ParticipanteService


equipes_bp = Blueprint(
    "equipes",
    __name__,
    url_prefix="/equipes",
)


hackathon_repository = HackathonRepository()
participante_repository = ParticipanteRepository()
equipe_repository = EquipeRepository()

service = EquipeService(
    equipe_repository,
    hackathon_repository,
    participante_repository,
)

hackathon_service = HackathonService(hackathon_repository)
participante_service = ParticipanteService(participante_repository)


@equipes_bp.route("/nova", methods=["GET", "POST"])
def criar():
    if request.method == "POST":
        hackathon_id = int(request.form["hackathon_id"])
        nome = request.form["nome"]
        participante_id = int(request.form["participante_id"])

        try:
            service.criar_equipe(
                hackathon_id,
                nome,
                participante_id,
            )

            flash("Equipe criada com sucesso.")

            return redirect(url_for("equipes.criar"))

        except (BusinessRuleError, NotFoundError) as error:
            flash(str(error))

    hackathons = hackathon_service.listar_hackathons()
    participantes = participante_service.listar_participantes()

    return render_template(
        "equipes/criar.html",
        hackathons=hackathons,
        participantes=participantes,
    )

@equipes_bp.route(
    "/adicionar-participante",
    methods=["GET", "POST"],
)
def adicionar_participante():
    if request.method == "POST":
        equipe_id = int(request.form["equipe_id"])
        participante_id = int(
            request.form["participante_id"]
        )

        try:
            service.adicionar_participante(
                equipe_id,
                participante_id,
            )

            flash(
                "Participante adicionado à equipe "
                "com sucesso."
            )

            return redirect(
                url_for("equipes.adicionar_participante")
            )

        except (BusinessRuleError, NotFoundError) as error:
            flash(str(error))

    equipes = service.listar_equipes()
    participantes = participante_service.listar_participantes()

    return render_template(
        "equipes/adicionar_participante.html",
        equipes=equipes,
        participantes=participantes,
    )

@equipes_bp.get("/")
def consultar():
    hackathons = hackathon_service.listar_hackathons()

    hackathon_id = request.args.get(
        "hackathon_id",
        type=int,
    )

    equipes = []

    if hackathon_id is not None:
        try:
            equipes = service.consultar_equipes(
                hackathon_id
            )

        except NotFoundError as error:
            flash(str(error))

    return render_template(
        "equipes/consultar.html",
        hackathons=hackathons,
        equipes=equipes,
        hackathon_id=hackathon_id,
    )