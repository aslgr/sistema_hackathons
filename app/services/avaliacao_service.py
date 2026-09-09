from app.domain.exceptions import BusinessRuleError, NotFoundError
from app.domain.models import Avaliacao
from app.repositories.avaliacao_repository import AvaliacaoRepository
from app.repositories.jurado_repository import JuradoRepository
from app.repositories.projeto_repository import ProjetoRepository


class AvaliacaoService:
    def __init__(
        self,
        jurado_repository: JuradoRepository,
        projeto_repository: ProjetoRepository,
        avaliacao_repository: AvaliacaoRepository,
    ):
        self.jurado_repository = jurado_repository
        self.projeto_repository = projeto_repository
        self.avaliacao_repository = avaliacao_repository

    def registrar_avaliacao(
        self,
        jurado_id: int,
        projeto_id: int,
        nota: float,
        comentario: str,
    ):
        if nota < 0 or nota > 10:
            raise BusinessRuleError(
                "A nota deve estar entre 0 e 10."
            )

        jurado = self.jurado_repository.buscar_por_id(
            jurado_id
        )

        if jurado is None:
            raise NotFoundError("Jurado não encontrado.")

        projeto = self.projeto_repository.buscar_por_id(
            projeto_id
        )

        if projeto is None:
            raise NotFoundError("Projeto não encontrado.")

        avaliacao_existente = (
            self.avaliacao_repository
            .buscar_por_jurado_e_projeto(
                jurado_id,
                projeto_id,
            )
        )

        if avaliacao_existente is not None:
            raise BusinessRuleError(
                "O jurado já avaliou este projeto."
            )

        avaliacao = Avaliacao(
            id=None,
            jurado=jurado,
            projeto=projeto,
            nota=nota,
            comentario=comentario,
        )

        return self.avaliacao_repository.salvar(avaliacao)

    def consultar_avaliacoes(self, projeto_id: int):
        projeto = self.projeto_repository.buscar_por_id(
            projeto_id
        )

        if projeto is None:
            raise NotFoundError("Projeto não encontrado.")

        return self.avaliacao_repository.listar_por_projeto(
            projeto_id
        )