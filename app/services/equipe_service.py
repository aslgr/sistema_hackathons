from app.domain.exceptions import BusinessRuleError, NotFoundError
from app.domain.models import Equipe, PapelUsuario
from app.repositories.equipe_repository import EquipeRepository
from app.repositories.hackathon_repository import HackathonRepository
from app.repositories.usuario_repository import UsuarioRepository


class EquipeService:
    def __init__(
        self,
        equipe_repository: EquipeRepository,
        hackathon_repository: HackathonRepository,
        usuario_repository: UsuarioRepository,
    ):
        self.equipe_repository = equipe_repository
        self.hackathon_repository = hackathon_repository
        self.usuario_repository = usuario_repository

    def criar_equipe(self, hackathon_id: int, nome: str, lider_id: int):
        nome = nome.strip()
        if not nome:
            raise BusinessRuleError("O nome da equipe é obrigatório.")

        hackathon = self.hackathon_repository.buscar_por_id(hackathon_id)
        if hackathon is None:
            raise NotFoundError("Hackathon não encontrado.")

        lider = self.usuario_repository.buscar_por_id(lider_id)
        if lider is None:
            raise NotFoundError("Participante não encontrado.")

        if lider.papel != PapelUsuario.PARTICIPANTE:
            raise BusinessRuleError("Somente participantes podem criar equipes.")

        if self.equipe_repository.contar_por_hackathon(hackathon_id) >= hackathon.max_equipes:
            raise BusinessRuleError("O limite máximo de equipes foi atingido.")

        if self.equipe_repository.participante_esta_em_hackathon(lider_id, hackathon_id):
            raise BusinessRuleError("O participante já pertence a uma equipe neste hackathon.")

        equipe = Equipe(
            id=None,
            nome=nome,
            hackathon=hackathon,
            lider=lider,
            participantes=[lider],
        )
        return self.equipe_repository.salvar(equipe)

    def adicionar_participante(
        self,
        equipe_id: int,
        participante_id: int,
        solicitante_id: int,
    ):
        equipe = self.equipe_repository.buscar_por_id(equipe_id)
        if equipe is None:
            raise NotFoundError("Equipe não encontrada.")

        if equipe.lider.id != solicitante_id:
            raise BusinessRuleError("Somente o líder da equipe pode adicionar participantes.")

        participante = self.usuario_repository.buscar_por_id(participante_id)
        if participante is None:
            raise NotFoundError("Participante não encontrado.")

        if participante.papel != PapelUsuario.PARTICIPANTE:
            raise BusinessRuleError("O usuário selecionado não é um participante.")

        if self.equipe_repository.participante_esta_em_hackathon(
            participante_id,
            equipe.hackathon.id,
        ):
            raise BusinessRuleError("O participante já pertence a uma equipe neste hackathon.")

        self.equipe_repository.adicionar_participante(equipe.id, participante.id)
        equipe.adicionar_participante(participante)
        return equipe

    def listar_equipes_do_lider(self, lider_id: int):
        return self.equipe_repository.listar_por_lider(lider_id)

    def consultar_equipes(self, hackathon_id: int):
        if self.hackathon_repository.buscar_por_id(hackathon_id) is None:
            raise NotFoundError("Hackathon não encontrado.")

        return self.equipe_repository.listar_por_hackathon(hackathon_id)
