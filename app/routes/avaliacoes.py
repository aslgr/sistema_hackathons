from flask import Blueprint, flash, redirect, render_template, request, url_for

from app.domain.exceptions import BusinessRuleError, NotFoundError
from app.repositories.avaliacao_repository import AvaliacaoRepository
from app.repositories.jurado_repository import JuradoRepository
from app.repositories.projeto_repository import ProjetoRepository
from app.services.avaliacao_service import AvaliacaoService
from app.services.jurado_service import JuradoService


avaliacoes_bp = Blueprint(
    "avaliacoes",
    __name__,
    url_prefix="/avaliacoes",
)


jurado_repository = JuradoRepository()
projeto_repository = ProjetoRepository()
avaliacao_repository = AvaliacaoRepository()

service = AvaliacaoService(
    jurado_repository,
    projeto_repository,
    avaliacao_repository,
)

jurado_service = JuradoService(jurado_repository)


@avaliacoes_bp.route("/nova", methods=["GET", "POST"])
def registrar():
    if request.method == "POST":
        jurado_id = int(request.form["jurado_id"])
        projeto_id = int(request.form["projeto_id"])
        nota = float(request.form["nota"])
        comentario = request.form["comentario"]

        try:
            service.registrar_avaliacao(
                jurado_id,
                projeto_id,
                nota,
                comentario,
            )

            flash("Avaliação registrada com sucesso.")

            return redirect(
                url_for("avaliacoes.registrar")
            )

        except (BusinessRuleError, NotFoundError) as error:
            flash(str(error))

    jurados = jurado_service.listar_jurados()
    projetos = projeto_repository.listar_todos()

    return render_template(
        "avaliacoes/registrar.html",
        jurados=jurados,
        projetos=projetos,
    )