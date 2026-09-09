from datetime import date

from app.domain.models import Hackathon
from app.repositories.hackathon_repository import HackathonRepository


class HackathonService:
    def __init__(self, repository: HackathonRepository):
        self.repository = repository

    def cadastrar_hackathon(
        self,
        nome: str,
        data_inicio: date,
        data_fim: date,
        max_equipes: int,
    ):
        hackathon = Hackathon(
            id=None,
            nome=nome,
            data_inicio=data_inicio,
            data_fim=data_fim,
            max_equipes=max_equipes,
        )

        return self.repository.salvar(hackathon)

    def listar_hackathons(self):
        return self.repository.listar_todos()