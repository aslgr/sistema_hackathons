from flask import Blueprint, flash, redirect, render_template, request, url_for

from app.domain.exceptions import NotFoundError
from app.repositories.equipe_repository import EquipeRepository
from app.repositories.mentor_repository import MentorRepository
from app.repositories.mentoria_repository import MentoriaRepository
from app.services.mentoria_service import MentoriaService
from app.services.mentor_service import MentorService


mentorias_bp = Blueprint(
    "mentorias",
    __name__,
    url_prefix="/mentorias",
)


mentor_repository = MentorRepository()
equipe_repository = EquipeRepository()
mentoria_repository = MentoriaRepository()

service = MentoriaService(
    mentor_repository,
    equipe_repository,
    mentoria_repository,
)

mentor_service = MentorService(mentor_repository)


@mentorias_bp.route("/nova", methods=["GET", "POST"])
def registrar():
    if request.method == "POST":
        mentor_id = int(request.form["mentor_id"])
        equipe_id = int(request.form["equipe_id"])
        comentario = request.form["comentario"]

        try:
            service.registrar_mentoria(
                mentor_id,
                equipe_id,
                comentario,
            )

            flash("Mentoria registrada com sucesso.")

            return redirect(
                url_for("mentorias.registrar")
            )

        except NotFoundError as error:
            flash(str(error))

    mentores = mentor_service.listar_mentores()
    equipes = equipe_repository.listar_todas()

    return render_template(
        "mentorias/registrar.html",
        mentores=mentores,
        equipes=equipes,
    )