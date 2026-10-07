from app.domain.exceptions import BusinessRuleError, NotFoundError
from app.domain.models import Avaliacao, PapelUsuario
from app.repositories.avaliacao_repository import AvaliacaoRepository
from app.repositories.hackathon_repository import HackathonRepository
from app.repositories.projeto_repository import ProjetoRepository
from app.repositories.usuario_repository import UsuarioRepository


class AvaliacaoService:
    def __init__(
        self,
        usuario_repository: UsuarioRepository,
        projeto_repository: ProjetoRepository,
        avaliacao_repository: AvaliacaoRepository,
        hackathon_repository: HackathonRepository,
    ):
        self.usuario_repository = usuario_repository
        self.projeto_repository = projeto_repository
        self.avaliacao_repository = avaliacao_repository
        self.hackathon_repository = hackathon_repository

    def registrar_avaliacao(
        self,
        jurado_id: int,
        projeto_id: int,
        nota: float,
        comentario: str,
    ):
        if nota < 0 or nota > 10:
            raise BusinessRuleError("A nota deve estar entre 0 e 10.")

        comentario = comentario.strip()
        if not comentario:
            raise BusinessRuleError("O comentário da avaliação é obrigatório.")

        jurado = self.usuario_repository.buscar_por_id(jurado_id)
        if jurado is None:
            raise NotFoundError("Jurado não encontrado.")

        if jurado.papel != PapelUsuario.JURADO:
            raise BusinessRuleError("O usuário não possui papel de jurado.")

        projeto = self.projeto_repository.buscar_por_id(projeto_id)
        if projeto is None:
            raise NotFoundError("Projeto não encontrado.")

        hackathon_id = projeto.equipe.hackathon.id
        if not self.hackathon_repository.jurado_associado(hackathon_id, jurado_id):
            raise BusinessRuleError(
                "O jurado não está associado ao hackathon deste projeto."
            )

        if self.avaliacao_repository.buscar_por_jurado_e_projeto(jurado_id, projeto_id):
            raise BusinessRuleError("O jurado já avaliou este projeto.")

        avaliacao = Avaliacao(
            id=None,
            jurado=jurado,
            projeto=projeto,
            nota=nota,
            comentario=comentario,
        )
        return self.avaliacao_repository.salvar(avaliacao)

    def consultar_avaliacoes(self, projeto_id: int):
        if self.projeto_repository.buscar_por_id(projeto_id) is None:
            raise NotFoundError("Projeto não encontrado.")

        return self.avaliacao_repository.listar_por_projeto(projeto_id)
