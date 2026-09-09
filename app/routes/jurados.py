from flask import Blueprint, flash, redirect, render_template, request, url_for

from app.repositories.jurado_repository import JuradoRepository
from app.services.jurado_service import JuradoService


jurados_bp = Blueprint(
    "jurados",
    __name__,
    url_prefix="/jurados",
)


repository = JuradoRepository()
service = JuradoService(repository)


@jurados_bp.route("/novo", methods=["GET", "POST"])
def cadastrar():
    if request.method == "POST":
        nome = request.form["nome"]
        email = request.form["email"]

        service.cadastrar_jurado(nome, email)

        flash("Jurado cadastrado com sucesso.")

        return redirect(url_for("jurados.cadastrar"))

    return render_template("jurados/cadastrar.html")