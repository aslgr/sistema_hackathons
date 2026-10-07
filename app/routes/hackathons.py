from datetime import date

from flask import Blueprint, flash, g, redirect, render_template, request, url_for

from app.auth.decorators import role_required
from app.domain.exceptions import BusinessRuleError, NotFoundError
from app.domain.models import PapelUsuario
from app.repositories.hackathon_repository import HackathonRepository
from app.repositories.usuario_repository import UsuarioRepository
from app.services.hackathon_service import HackathonService


hackathons_bp = Blueprint("hackathons", __name__, url_prefix="/hackathons")

hackathon_service = HackathonService(HackathonRepository(), UsuarioRepository())


@hackathons_bp.route("/novo", methods=["GET", "POST"])
@role_required(PapelUsuario.ORGANIZADOR)
def cadastrar():
    if request.method == "POST":
        try:
            hackathon_service.cadastrar_hackathon(
                nome=request.form["nome"],
                data_inicio=date.fromisoformat(request.form["data_inicio"]),
                data_fim=date.fromisoformat(request.form["data_fim"]),
                max_equipes=int(request.form["max_equipes"]),
                organizador_id=g.usuario.id,
            )
        except ValueError:
            flash("Informe datas e limite de equipes válidos.")
        except (BusinessRuleError, NotFoundError) as error:
            flash(str(error))
        else:
            flash("Hackathon cadastrado com sucesso.")
            return redirect(url_for("hackathons.cadastrar"))

    return render_template("hackathons/cadastrar.html")
