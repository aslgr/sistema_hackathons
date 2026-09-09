from datetime import date

from flask import Blueprint, flash, redirect, render_template, request, url_for

from app.repositories.hackathon_repository import HackathonRepository
from app.services.hackathon_service import HackathonService


hackathons_bp = Blueprint(
    "hackathons",
    __name__,
    url_prefix="/hackathons",
)


repository = HackathonRepository()
service = HackathonService(repository)


@hackathons_bp.route("/novo", methods=["GET", "POST"])
def cadastrar():
    if request.method == "POST":
        nome = request.form["nome"]
        data_inicio = date.fromisoformat(request.form["data_inicio"])
        data_fim = date.fromisoformat(request.form["data_fim"])
        max_equipes = int(request.form["max_equipes"])

        service.cadastrar_hackathon(
            nome,
            data_inicio,
            data_fim,
            max_equipes,
        )

        flash("Hackathon cadastrado com sucesso.")

        return redirect(url_for("hackathons.cadastrar"))

    return render_template("hackathons/cadastrar.html")