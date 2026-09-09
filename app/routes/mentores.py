from flask import Blueprint, flash, redirect, render_template, request, url_for

from app.repositories.mentor_repository import MentorRepository
from app.services.mentor_service import MentorService


mentores_bp = Blueprint(
    "mentores",
    __name__,
    url_prefix="/mentores",
)


repository = MentorRepository()
service = MentorService(repository)


@mentores_bp.route("/novo", methods=["GET", "POST"])
def cadastrar():
    if request.method == "POST":
        nome = request.form["nome"]
        email = request.form["email"]

        service.cadastrar_mentor(nome, email)

        flash("Mentor cadastrado com sucesso.")

        return redirect(url_for("mentores.cadastrar"))

    return render_template("mentores/cadastrar.html")