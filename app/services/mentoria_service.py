from app.domain.exceptions import BusinessRuleError, NotFoundError
from app.domain.models import Mentoria, PapelUsuario
from app.repositories.equipe_repository import EquipeRepository
from app.repositories.hackathon_repository import HackathonRepository
from app.repositories.mentoria_repository import MentoriaRepository
from app.repositories.usuario_repository import UsuarioRepository


class MentoriaService:
    def __init__(
        self,
        usuario_repository: UsuarioRepository,
        equipe_repository: EquipeRepository,
        mentoria_repository: MentoriaRepository,
        hackathon_repository: HackathonRepository,
    ):
        self.usuario_repository = usuario_repository
        self.equipe_repository = equipe_repository
        self.mentoria_repository = mentoria_repository
        self.hackathon_repository = hackathon_repository

    def registrar_mentoria(self, mentor_id: int, equipe_id: int, comentario: str):
        comentario = comentario.strip()
        if not comentario:
            raise BusinessRuleError("O comentário da mentoria é obrigatório.")

        mentor = self.usuario_repository.buscar_por_id(mentor_id)
        if mentor is None:
            raise NotFoundError("Mentor não encontrado.")

        if mentor.papel != PapelUsuario.MENTOR:
            raise BusinessRuleError("O usuário não possui papel de mentor.")

        equipe = self.equipe_repository.buscar_por_id(equipe_id)
        if equipe is None:
            raise NotFoundError("Equipe não encontrada.")

        if not self.hackathon_repository.mentor_associado(equipe.hackathon.id, mentor_id):
            raise BusinessRuleError(
                "O mentor não está associado ao hackathon desta equipe."
            )

        mentoria = Mentoria(
            id=None,
            mentor=mentor,
            equipe=equipe,
            comentario=comentario,
        )
        return self.mentoria_repository.salvar(mentoria)

    def consultar_mentorias(self, participante_id: int, equipe_id: int):
        participante = self.usuario_repository.buscar_por_id(participante_id)
        if participante is None:
            raise NotFoundError("Participante não encontrado.")

        if participante.papel != PapelUsuario.PARTICIPANTE:
            raise BusinessRuleError("O usuário não possui papel de participante.")

        equipe = self.equipe_repository.buscar_por_id(equipe_id)
        if equipe is None:
            raise NotFoundError("Equipe não encontrada.")

        if not self.equipe_repository.participante_esta_na_equipe(
            participante_id,
            equipe_id,
        ):
            raise BusinessRuleError(
                "Você não pertence a esta equipe."
            )

        return self.mentoria_repository.listar_por_equipe(equipe_id)
