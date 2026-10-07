from werkzeug.security import check_password_hash, generate_password_hash

from app.domain.exceptions import BusinessRuleError
from app.domain.models import PapelUsuario, Usuario
from app.repositories.usuario_repository import UsuarioRepository


class UsuarioService:
    PAPEIS_COLABORADORES = {PapelUsuario.JURADO, PapelUsuario.MENTOR}

    def __init__(self, repository: UsuarioRepository):
        self.repository = repository

    def cadastrar_organizador(self, nome: str, email: str, senha: str):
        return self._cadastrar_usuario(nome, email, senha, PapelUsuario.ORGANIZADOR)

    def cadastrar_participante(self, nome: str, email: str, senha: str):
        return self._cadastrar_usuario(nome, email, senha, PapelUsuario.PARTICIPANTE)

    def cadastrar_colaborador(self, nome: str, email: str, senha: str, papel: str):
        try:
            papel_usuario = PapelUsuario(papel)
        except ValueError as error:
            raise BusinessRuleError("Papel de usuário inválido.") from error

        if papel_usuario not in self.PAPEIS_COLABORADORES:
            raise BusinessRuleError("Apenas jurados e mentores podem ser colaboradores.")

        return self._cadastrar_usuario(nome, email, senha, papel_usuario)

    def autenticar(self, email: str, senha: str):
        email = email.strip().lower()
        usuario = self.repository.buscar_por_email(email)

        if usuario is None or not check_password_hash(usuario.senha_hash, senha):
            raise BusinessRuleError("E-mail ou senha inválidos.")

        return usuario

    def listar_por_papel(self, papel: PapelUsuario):
        return self.repository.listar_por_papel(papel)

    def listar_colaboradores(self):
        colaboradores = []
        for papel in (PapelUsuario.JURADO, PapelUsuario.MENTOR):
            colaboradores.extend(self.repository.listar_por_papel(papel))

        return sorted(colaboradores, key=lambda usuario: usuario.nome.casefold())

    def _cadastrar_usuario(
        self,
        nome: str,
        email: str,
        senha: str,
        papel: PapelUsuario,
    ):
        nome = nome.strip()
        email = email.strip().lower()

        if not nome:
            raise BusinessRuleError("O nome é obrigatório.")

        if not email or "@" not in email:
            raise BusinessRuleError("Informe um e-mail válido.")

        if len(senha) < 8:
            raise BusinessRuleError("A senha deve possuir pelo menos 8 caracteres.")

        if self.repository.buscar_por_email(email):
            raise BusinessRuleError("Já existe um usuário cadastrado com este e-mail.")

        usuario = Usuario(
            id=None,
            nome=nome,
            email=email,
            senha_hash=generate_password_hash(senha),
            papel=papel,
        )
        return self.repository.salvar(usuario)
