from app.domain.exceptions import BusinessRuleError, NotFoundError
from app.domain.models import Projeto
from app.repositories.equipe_repository import EquipeRepository
from app.repositories.hackathon_repository import HackathonRepository
from app.repositories.projeto_repository import ProjetoRepository


class ProjetoService:
    def __init__(
        self,
        equipe_repository: EquipeRepository,
        projeto_repository: ProjetoRepository,
        hackathon_repository: HackathonRepository,
    ):
        self.equipe_repository = equipe_repository
        self.projeto_repository = projeto_repository
        self.hackathon_repository = hackathon_repository

    def registrar_projeto(
        self,
        equipe_id: int,
        titulo: str,
        descricao: str,
        area_tematica: str,
        solicitante_id: int,
    ):
        equipe = self.equipe_repository.buscar_por_id(equipe_id)
        if equipe is None:
            raise NotFoundError("Equipe não encontrada.")

        if equipe.lider.id != solicitante_id:
            raise BusinessRuleError("Somente o líder da equipe pode registrar o projeto.")

        if self.projeto_repository.existe_para_equipe(equipe_id):
            raise BusinessRuleError("A equipe já possui um projeto registrado.")

        titulo = titulo.strip()
        descricao = descricao.strip()
        area_tematica = area_tematica.strip()

        if not titulo or not descricao or not area_tematica:
            raise BusinessRuleError("Todos os dados do projeto são obrigatórios.")

        projeto = Projeto(
            id=None,
            titulo=titulo,
            descricao=descricao,
            area_tematica=area_tematica,
            equipe=equipe,
        )
        return self.projeto_repository.salvar(projeto)

    def consultar_projetos(self, hackathon_id: int):
        if self.hackathon_repository.buscar_por_id(hackathon_id) is None:
            raise NotFoundError("Hackathon não encontrado.")

        return self.projeto_repository.listar_por_hackathon(hackathon_id)
