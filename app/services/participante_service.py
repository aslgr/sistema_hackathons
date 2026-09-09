from app.domain.models import Participante
from app.repositories.participante_repository import ParticipanteRepository


class ParticipanteService:
    def __init__(self, repository: ParticipanteRepository):
        self.repository = repository

    def cadastrar_participante(self, nome: str, email: str):
        participante = Participante(
            id=None,
            nome=nome,
            email=email,
        )

        return self.repository.salvar(participante)

    def listar_participantes(self):
        return self.repository.listar_todos()