from flask import Blueprint, flash, render_template, request

from app.domain.exceptions import NotFoundError
from app.repositories.avaliacao_repository import AvaliacaoRepository
from app.repositories.hackathon_repository import HackathonRepository
from app.repositories.projeto_repository import ProjetoRepository
from app.services.classificacao_service import ClassificacaoService
from app.services.hackathon_service import HackathonService


classificacao_bp = Blueprint(
    "classificacao",
    __name__,
    url_prefix="/classificacao",
)


hackathon_repository = HackathonRepository()
projeto_repository = ProjetoRepository()
avaliacao_repository = AvaliacaoRepository()

service = ClassificacaoService(
    hackathon_repository,
    projeto_repository,
    avaliacao_repository,
)

hackathon_service = HackathonService(
    hackathon_repository
)


@classificacao_bp.get("/")
def consultar():
    hackathons = hackathon_service.listar_hackathons()

    hackathon_id = request.args.get(
        "hackathon_id",
        type=int,
    )

    classificacao = []

    if hackathon_id is not None:
        try:
            classificacao = (
                service.consultar_classificacao(
                    hackathon_id
                )
            )

        except NotFoundError as error:
            flash(str(error))

    return render_template(
        "classificacao/consultar.html",
        hackathons=hackathons,
        classificacao=classificacao,
        hackathon_id=hackathon_id,
    )