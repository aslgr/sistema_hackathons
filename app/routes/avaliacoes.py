from flask import Blueprint, flash, g, redirect, render_template, request, url_for

from app.auth.decorators import role_required
from app.domain.exceptions import BusinessRuleError, NotFoundError
from app.domain.models import PapelUsuario
from app.repositories.avaliacao_repository import AvaliacaoRepository
from app.repositories.hackathon_repository import HackathonRepository
from app.repositories.projeto_repository import ProjetoRepository
from app.repositories.usuario_repository import UsuarioRepository
from app.services.avaliacao_service import AvaliacaoService


avaliacoes_bp = Blueprint("avaliacoes", __name__, url_prefix="/avaliacoes")

hackathon_repository = HackathonRepository()
projeto_repository = ProjetoRepository()
avaliacao_service = AvaliacaoService(
    UsuarioRepository(),
    projeto_repository,
    AvaliacaoRepository(),
    hackathon_repository,
)


@avaliacoes_bp.route("/nova", methods=["GET", "POST"])
@role_required(PapelUsuario.JURADO)
def registrar():
    if request.method == "POST":
        try:
            avaliacao_service.registrar_avaliacao(
                jurado_id=g.usuario.id,
                projeto_id=int(request.form["projeto_id"]),
                nota=float(request.form["nota"]),
                comentario=request.form["comentario"],
            )
        except ValueError:
            flash("Selecione um projeto e informe uma nota válida.")
        except (BusinessRuleError, NotFoundError) as error:
            flash(str(error))
        else:
            flash("Avaliação registrada com sucesso.")
            return redirect(url_for("avaliacoes.registrar"))

    return render_template(
        "avaliacoes/registrar.html",
        projetos=projeto_repository.listar_para_jurado(g.usuario.id),
    )


@avaliacoes_bp.get("/")
def consultar():
    hackathon_id = request.args.get("hackathon_id", type=int)
    projeto_id = request.args.get("projeto_id", type=int)

    hackathon_selecionado = None
    projeto_selecionado = None
    projetos = []
    avaliacoes = []

    if hackathon_id is not None:
        hackathon_selecionado = hackathon_repository.buscar_por_id(hackathon_id)

        if hackathon_selecionado is None:
            flash("Hackathon não encontrado.")
        else:
            projetos = projeto_repository.listar_por_hackathon(hackathon_id)

    if projeto_id is not None:
        projeto_selecionado = projeto_repository.buscar_por_id(projeto_id)

        if projeto_selecionado is None:
            flash("Projeto não encontrado.")
        elif (
            hackathon_selecionado is None
            or projeto_selecionado.equipe.hackathon.id != hackathon_id
        ):
            flash("O projeto não pertence ao hackathon selecionado.")
            projeto_selecionado = None
        else:
            avaliacoes = avaliacao_service.consultar_avaliacoes(projeto_id)

    return render_template(
        "avaliacoes/consultar.html",
        hackathons=hackathon_repository.listar_todos(),
        hackathon_id=hackathon_id,
        hackathon_selecionado=hackathon_selecionado,
        projetos=projetos,
        projeto_id=projeto_id,
        projeto_selecionado=projeto_selecionado,
        avaliacoes=avaliacoes,
    )
