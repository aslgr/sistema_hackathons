from app.domain.exceptions import NotFoundError
from app.repositories.avaliacao_repository import AvaliacaoRepository
from app.repositories.hackathon_repository import HackathonRepository
from app.repositories.projeto_repository import ProjetoRepository


class ClassificacaoService:
    def __init__(
        self,
        hackathon_repository: HackathonRepository,
        projeto_repository: ProjetoRepository,
        avaliacao_repository: AvaliacaoRepository,
    ):
        self.hackathon_repository = hackathon_repository
        self.projeto_repository = projeto_repository
        self.avaliacao_repository = avaliacao_repository

    def consultar_classificacao(self, hackathon_id: int):
        if self.hackathon_repository.buscar_por_id(hackathon_id) is None:
            raise NotFoundError("Hackathon não encontrado.")

        projetos = self.projeto_repository.listar_por_hackathon(hackathon_id)
        avaliacoes = self.avaliacao_repository.listar_por_hackathon(hackathon_id)
        return self._calcular_classificacao(projetos, avaliacoes)

    @staticmethod
    def _calcular_classificacao(projetos, avaliacoes):
        notas_por_projeto = {}

        for avaliacao in avaliacoes:
            notas_por_projeto.setdefault(avaliacao["projeto_id"], []).append(
                avaliacao["nota"]
            )

        classificacao = []
        for projeto in projetos:
            notas = notas_por_projeto.get(projeto.id, [])
            if not notas:
                continue

            classificacao.append(
                {
                    "projeto": projeto,
                    "media": sum(notas) / len(notas),
                }
            )

        classificacao.sort(key=lambda item: item["media"], reverse=True)

        posicao_atual = 0
        media_anterior = None
        for indice, item in enumerate(classificacao, start=1):
            if media_anterior is None or item["media"] != media_anterior:
                posicao_atual = indice

            item["posicao"] = posicao_atual
            media_anterior = item["media"]

        return classificacao
