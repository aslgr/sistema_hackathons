from flask import Blueprint, flash, g, redirect, render_template, request, url_for

from app.auth.decorators import role_required
from app.domain.exceptions import BusinessRuleError, NotFoundError
from app.domain.models import PapelUsuario
from app.repositories.equipe_repository import EquipeRepository
from app.repositories.hackathon_repository import HackathonRepository
from app.repositories.mentoria_repository import MentoriaRepository
from app.repositories.usuario_repository import UsuarioRepository
from app.services.mentoria_service import MentoriaService


mentorias_bp = Blueprint("mentorias", __name__, url_prefix="/mentorias")

usuario_repository = UsuarioRepository()
equipe_repository = EquipeRepository()
mentoria_service = MentoriaService(
    usuario_repository,
    equipe_repository,
    MentoriaRepository(),
    HackathonRepository(),
)


@mentorias_bp.route("/nova", methods=["GET", "POST"])
@role_required(PapelUsuario.MENTOR)
def registrar():
    if request.method == "POST":
        try:
            mentoria_service.registrar_mentoria(
                mentor_id=g.usuario.id,
                equipe_id=int(request.form["equipe_id"]),
                comentario=request.form["comentario"],
            )
        except ValueError:
            flash("Selecione uma equipe válida.")
        except (BusinessRuleError, NotFoundError) as error:
            flash(str(error))
        else:
            flash("Mentoria registrada com sucesso.")
            return redirect(url_for("mentorias.registrar"))

    return render_template(
        "mentorias/registrar.html",
        equipes=equipe_repository.listar_para_mentor(g.usuario.id),
    )


@mentorias_bp.get("/")
@role_required(PapelUsuario.PARTICIPANTE)
def consultar():
    equipes = equipe_repository.listar_por_participante(
        g.usuario.id
    )

    equipe_id = request.args.get(
        "equipe_id",
        type=int,
    )

    mentorias = []
    equipe_selecionada = None

    if equipe_id is not None:
        try:
            mentorias = mentoria_service.consultar_mentorias(
                g.usuario.id,
                equipe_id,
            )

            equipe_selecionada = equipe_repository.buscar_por_id(
                equipe_id
            )

        except (
            BusinessRuleError,
            NotFoundError,
        ) as error:
            flash(str(error))

    return render_template(
        "mentorias/consultar.html",
        equipes=equipes,
        mentorias=mentorias,
        equipe_id=equipe_id,
        equipe_selecionada=equipe_selecionada,
    )