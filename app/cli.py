import click
from flask.cli import with_appcontext

from app.domain.exceptions import BusinessRuleError
from app.repositories.usuario_repository import UsuarioRepository
from app.services.usuario_service import UsuarioService


@click.command("criar-organizador")
@click.option("--nome", prompt="Nome")
@click.option("--email", prompt="E-mail")
@click.option(
    "--senha",
    prompt="Senha",
    hide_input=True,
    confirmation_prompt="Confirme a senha",
)
@with_appcontext
def criar_organizador_command(nome: str, email: str, senha: str):
    """Cria a primeira conta de organizador da aplicação."""
    service = UsuarioService(UsuarioRepository())

    try:
        usuario = service.cadastrar_organizador(nome, email, senha)
    except BusinessRuleError as error:
        raise click.ClickException(str(error)) from error

    click.echo(f"Organizador '{usuario.nome}' criado com sucesso.")


def init_app(app):
    app.cli.add_command(criar_organizador_command)
