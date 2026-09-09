from app.domain.exceptions import BusinessRuleError, NotFoundError
from app.domain.models import Projeto
from app.repositories.equipe_repository import EquipeRepository
from app.repositories.projeto_repository import ProjetoRepository


class ProjetoService:
    def __init__(
        self,
        equipe_repository: EquipeRepository,
        projeto_repository: ProjetoRepository,
    ):
        self.equipe_repository = equipe_repository
        self.projeto_repository = projeto_repository

    def registrar_projeto(
        self,
        equipe_id: int,
        titulo: str,
        descricao: str,
        area_tematica: str,
    ):
        equipe = self.equipe_repository.buscar_por_id(
            equipe_id
        )

        if equipe is None:
            raise NotFoundError("Equipe não encontrada.")

        projeto_existente = (
            self.projeto_repository.buscar_por_equipe(
                equipe_id
            )
        )

        if projeto_existente is not None:
            raise BusinessRuleError(
                "A equipe já possui um projeto registrado."
            )

        projeto = Projeto(
            id=None,
            titulo=titulo,
            descricao=descricao,
            area_tematica=area_tematica,
            equipe=equipe,
        )

        return self.projeto_repository.salvar(projeto)