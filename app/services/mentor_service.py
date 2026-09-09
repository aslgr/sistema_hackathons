from app.domain.models import Mentor
from app.repositories.mentor_repository import MentorRepository


class MentorService:
    def __init__(self, repository: MentorRepository):
        self.repository = repository

    def cadastrar_mentor(self, nome: str, email: str):
        mentor = Mentor(
            id=None,
            nome=nome,
            email=email,
        )

        return self.repository.salvar(mentor)

    def listar_mentores(self):
        return self.repository.listar_todos()