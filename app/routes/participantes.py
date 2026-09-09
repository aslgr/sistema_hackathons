from flask import Blueprint, flash, redirect, render_template, request, url_for

from app.repositories.participante_repository import ParticipanteRepository
from app.services.participante_service import ParticipanteService


participantes_bp = Blueprint(
    "participantes",
    __name__,
    url_prefix="/participantes",
)


repository = ParticipanteRepository()
service = ParticipanteService(repository)


@participantes_bp.route("/novo", methods=["GET", "POST"])
def cadastrar():
    if request.method == "POST":
        nome = request.form["nome"]
        email = request.form["email"]

        service.cadastrar_participante(nome, email)

        flash("Participante cadastrado com sucesso.")

        return redirect(url_for("participantes.cadastrar"))

    return render_template("participantes/cadastrar.html")