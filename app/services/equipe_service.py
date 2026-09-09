from app.domain.exceptions import BusinessRuleError, NotFoundError
from app.domain.models import Equipe
from app.repositories.equipe_repository import EquipeRepository
from app.repositories.hackathon_repository import HackathonRepository
from app.repositories.participante_repository import ParticipanteRepository


class EquipeService:
    def __init__(
        self,
        equipe_repository: EquipeRepository,
        hackathon_repository: HackathonRepository,
        participante_repository: ParticipanteRepository,
    ):
        self.equipe_repository = equipe_repository
        self.hackathon_repository = hackathon_repository
        self.participante_repository = participante_repository

    def criar_equipe(
        self,
        hackathon_id: int,
        nome: str,
        participante_id: int,
    ):
        hackathon = self.hackathon_repository.buscar_por_id(
            hackathon_id
        )

        if hackathon is None:
            raise NotFoundError("Hackathon não encontrado.")

        participante = self.participante_repository.buscar_por_id(
            participante_id
        )

        if participante is None:
            raise NotFoundError("Participante não encontrado.")

        quantidade_equipes = (
            self.equipe_repository.contar_por_hackathon(
                hackathon_id
            )
        )

        if quantidade_equipes >= hackathon.max_equipes:
            raise BusinessRuleError(
                "O limite máximo de equipes foi atingido."
            )

        equipe_existente = (
            self.equipe_repository
            .buscar_por_participante_e_hackathon(
                participante_id,
                hackathon_id,
            )
        )

        if equipe_existente is not None:
            raise BusinessRuleError(
                "O participante já pertence a uma equipe "
                "neste hackathon."
            )

        equipe = Equipe(
            id=None,
            nome=nome,
            hackathon=hackathon,
            participantes=[participante],
        )

        return self.equipe_repository.salvar(equipe)

    def adicionar_participante(
        self,
        equipe_id: int,
        participante_id: int,
    ):
        equipe = self.equipe_repository.buscar_por_id(
            equipe_id
        )

        if equipe is None:
            raise NotFoundError("Equipe não encontrada.")

        participante = self.participante_repository.buscar_por_id(
            participante_id
        )

        if participante is None:
            raise NotFoundError("Participante não encontrado.")

        equipe_existente = (
            self.equipe_repository
            .buscar_por_participante_e_hackathon(
                participante_id,
                equipe.hackathon.id,
            )
        )

        if equipe_existente is not None:
            raise BusinessRuleError(
                "O participante já pertence a uma equipe "
                "neste hackathon."
            )

        equipe.adicionar_participante(participante)

        self.equipe_repository.adicionar_participante(
            equipe_id,
            participante_id,
        )

        return equipe


    def listar_equipes(self):
        return self.equipe_repository.listar_todas()