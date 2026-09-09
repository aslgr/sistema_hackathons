from app.domain.exceptions import NotFoundError
from app.domain.models import Mentoria
from app.repositories.equipe_repository import EquipeRepository
from app.repositories.mentor_repository import MentorRepository
from app.repositories.mentoria_repository import MentoriaRepository


class MentoriaService:
    def __init__(
        self,
        mentor_repository: MentorRepository,
        equipe_repository: EquipeRepository,
        mentoria_repository: MentoriaRepository,
    ):
        self.mentor_repository = mentor_repository
        self.equipe_repository = equipe_repository
        self.mentoria_repository = mentoria_repository

    def registrar_mentoria(
        self,
        mentor_id: int,
        equipe_id: int,
        comentario: str,
    ):
        mentor = self.mentor_repository.buscar_por_id(
            mentor_id
        )

        if mentor is None:
            raise NotFoundError("Mentor não encontrado.")

        equipe = self.equipe_repository.buscar_por_id(
            equipe_id
        )

        if equipe is None:
            raise NotFoundError("Equipe não encontrada.")

        mentoria = Mentoria(
            id=None,
            mentor=mentor,
            equipe=equipe,
            comentario=comentario,
        )

        return self.mentoria_repository.salvar(mentoria)