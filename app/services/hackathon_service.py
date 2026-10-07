from datetime import date

from app.domain.exceptions import BusinessRuleError, NotFoundError
from app.domain.models import Hackathon, PapelUsuario
from app.repositories.hackathon_repository import HackathonRepository
from app.repositories.usuario_repository import UsuarioRepository


class HackathonService:
    def __init__(
        self,
        repository: HackathonRepository,
        usuario_repository: UsuarioRepository,
    ):
        self.repository = repository
        self.usuario_repository = usuario_repository

    def cadastrar_hackathon(
        self,
        nome: str,
        data_inicio: date,
        data_fim: date,
        max_equipes: int,
        organizador_id: int,
    ):
        nome = nome.strip()

        if not nome:
            raise BusinessRuleError("O nome é obrigatório.")

        if data_fim < data_inicio:
            raise BusinessRuleError("A data final não pode ser anterior à data inicial.")

        if max_equipes <= 0:
            raise BusinessRuleError("O número máximo de equipes deve ser maior que zero.")

        organizador = self._buscar_usuario_com_papel(
            organizador_id,
            PapelUsuario.ORGANIZADOR,
            "Organizador não encontrado.",
        )

        hackathon = Hackathon(
            id=None,
            nome=nome,
            data_inicio=data_inicio,
            data_fim=data_fim,
            max_equipes=max_equipes,
            organizador=organizador,
        )
        return self.repository.salvar(hackathon)

    def associar_jurado(self, hackathon_id: int, jurado_id: int, organizador_id: int):
        hackathon = self._buscar_hackathon_do_organizador(hackathon_id, organizador_id)
        jurado = self._buscar_usuario_com_papel(
            jurado_id,
            PapelUsuario.JURADO,
            "Jurado não encontrado.",
        )

        if self.repository.jurado_associado(hackathon.id, jurado.id):
            raise BusinessRuleError("O jurado já está associado a este hackathon.")

        self.repository.associar_jurado(hackathon.id, jurado.id)

    def associar_mentor(self, hackathon_id: int, mentor_id: int, organizador_id: int):
        hackathon = self._buscar_hackathon_do_organizador(hackathon_id, organizador_id)
        mentor = self._buscar_usuario_com_papel(
            mentor_id,
            PapelUsuario.MENTOR,
            "Mentor não encontrado.",
        )

        if self.repository.mentor_associado(hackathon.id, mentor.id):
            raise BusinessRuleError("O mentor já está associado a este hackathon.")

        self.repository.associar_mentor(hackathon.id, mentor.id)

    def listar_hackathons(self):
        return self.repository.listar_todos()

    def listar_por_organizador(self, organizador_id: int):
        return self.repository.listar_por_organizador(organizador_id)

    def _buscar_hackathon_do_organizador(self, hackathon_id: int, organizador_id: int):
        hackathon = self.repository.buscar_por_id(hackathon_id)

        if hackathon is None:
            raise NotFoundError("Hackathon não encontrado.")

        if hackathon.organizador.id != organizador_id:
            raise BusinessRuleError("Somente o organizador do hackathon pode alterá-lo.")

        return hackathon

    def _buscar_usuario_com_papel(
        self,
        usuario_id: int,
        papel: PapelUsuario,
        mensagem_nao_encontrado: str,
    ):
        usuario = self.usuario_repository.buscar_por_id(usuario_id)

        if usuario is None:
            raise NotFoundError(mensagem_nao_encontrado)

        if usuario.papel != papel:
            raise BusinessRuleError(f"O usuário não possui papel de {papel.rotulo.lower()}.")

        return usuario
