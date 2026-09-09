from app.domain.models import Jurado
from app.repositories.jurado_repository import JuradoRepository


class JuradoService:
    def __init__(self, repository: JuradoRepository):
        self.repository = repository

    def cadastrar_jurado(self, nome: str, email: str):
        jurado = Jurado(
            id=None,
            nome=nome,
            email=email,
        )

        return self.repository.salvar(jurado)

    def listar_jurados(self):
        return self.repository.listar_todos()