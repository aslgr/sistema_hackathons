from flask import Blueprint, flash, render_template, request

from app.domain.exceptions import NotFoundError
from app.repositories.avaliacao_repository import AvaliacaoRepository
from app.repositories.hackathon_repository import HackathonRepository
from app.repositories.projeto_repository import ProjetoRepository
from app.services.classificacao_service import ClassificacaoService


classificacao_bp = Blueprint("classificacao", __name__, url_prefix="/classificacao")

hackathon_repository = HackathonRepository()
classificacao_service = ClassificacaoService(
    hackathon_repository,
    ProjetoRepository(),
    AvaliacaoRepository(),
)


@classificacao_bp.get("/")
def consultar():
    hackathon_id = request.args.get("hackathon_id", type=int)
    classificacao = []

    if hackathon_id is not None:
        try:
            classificacao = classificacao_service.consultar_classificacao(hackathon_id)
        except NotFoundError as error:
            flash(str(error))

    return render_template(
        "classificacao/consultar.html",
        hackathons=hackathon_repository.listar_todos(),
        classificacao=classificacao,
        hackathon_id=hackathon_id,
    )
