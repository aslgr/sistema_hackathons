import tempfile
import unittest
from datetime import date
from pathlib import Path

from app import create_app
from app.database.connection import init_db
from app.domain.exceptions import BusinessRuleError
from app.repositories.avaliacao_repository import AvaliacaoRepository
from app.repositories.equipe_repository import EquipeRepository
from app.repositories.hackathon_repository import HackathonRepository
from app.repositories.mentoria_repository import MentoriaRepository
from app.repositories.projeto_repository import ProjetoRepository
from app.repositories.usuario_repository import UsuarioRepository
from app.services.avaliacao_service import AvaliacaoService
from app.services.classificacao_service import ClassificacaoService
from app.services.equipe_service import EquipeService
from app.services.hackathon_service import HackathonService
from app.services.mentoria_service import MentoriaService
from app.services.projeto_service import ProjetoService
from app.services.usuario_service import UsuarioService


class FluxoIntegradoTestCase(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        database_path = Path(self.temp_dir.name) / "test.sqlite3"

        self.app = create_app(
            {
                "TESTING": True,
                "DATABASE": str(database_path),
                "SECRET_KEY": "test-secret-key",
            }
        )

        with self.app.app_context():
            init_db()
            self._criar_dados_base()

    def tearDown(self):
        self.temp_dir.cleanup()

    def _criar_dados_base(self):
        usuario_repository = UsuarioRepository()
        hackathon_repository = HackathonRepository()
        equipe_repository = EquipeRepository()
        projeto_repository = ProjetoRepository()
        avaliacao_repository = AvaliacaoRepository()

        usuario_service = UsuarioService(usuario_repository)
        hackathon_service = HackathonService(hackathon_repository, usuario_repository)
        equipe_service = EquipeService(
            equipe_repository,
            hackathon_repository,
            usuario_repository,
        )
        projeto_service = ProjetoService(
            equipe_repository,
            projeto_repository,
            hackathon_repository,
        )
        avaliacao_service = AvaliacaoService(
            usuario_repository,
            projeto_repository,
            avaliacao_repository,
            hackathon_repository,
        )
        mentoria_service = MentoriaService(
            usuario_repository,
            equipe_repository,
            MentoriaRepository(),
            hackathon_repository,
        )

        self.organizador = usuario_service.cadastrar_organizador(
            "Arthur Organizador",
            "organizador@teste.com",
            "12345678",
        )
        self.participante = usuario_service.cadastrar_participante(
            "Pedro Participante",
            "pedro@teste.com",
            "12345678",
        )
        self.segundo_participante = usuario_service.cadastrar_participante(
            "Ana Participante",
            "ana@teste.com",
            "12345678",
        )
        self.jurado = usuario_service.cadastrar_colaborador(
            "João Jurado",
            "jurado@teste.com",
            "12345678",
            "JURADO",
        )
        self.mentor = usuario_service.cadastrar_colaborador(
            "Maria Mentor",
            "mentor@teste.com",
            "12345678",
            "MENTOR",
        )

        self.hackathon = hackathon_service.cadastrar_hackathon(
            "Hackathon UFPR",
            date(2026, 10, 10),
            date(2026, 10, 12),
            10,
            self.organizador.id,
        )
        hackathon_service.associar_jurado(
            self.hackathon.id,
            self.jurado.id,
            self.organizador.id,
        )
        hackathon_service.associar_mentor(
            self.hackathon.id,
            self.mentor.id,
            self.organizador.id,
        )

        self.equipe = equipe_service.criar_equipe(
            self.hackathon.id,
            "Equipe Alpha",
            self.participante.id,
        )
        equipe_service.adicionar_participante(
            self.equipe.id,
            self.segundo_participante.id,
            self.participante.id,
        )

        self.projeto = projeto_service.registrar_projeto(
            self.equipe.id,
            "EcoTrack",
            "Plataforma para monitoramento ambiental.",
            "Sustentabilidade",
            self.participante.id,
        )

        self.avaliacao = avaliacao_service.registrar_avaliacao(
            self.jurado.id,
            self.projeto.id,
            8.5,
            "Boa proposta e execução consistente.",
        )
        self.mentoria = mentoria_service.registrar_mentoria(
            self.mentor.id,
            self.equipe.id,
            "Validar a proposta com usuários.",
        )

    def test_fluxo_completo_calcula_classificacao(self):
        with self.app.app_context():
            classificacao = ClassificacaoService(
                HackathonRepository(),
                ProjetoRepository(),
                AvaliacaoRepository(),
            ).consultar_classificacao(self.hackathon.id)

            self.assertEqual(len(classificacao), 1)
            self.assertEqual(classificacao[0]["posicao"], 1)
            self.assertEqual(classificacao[0]["projeto"].titulo, "EcoTrack")
            self.assertAlmostEqual(classificacao[0]["media"], 8.5)

    def test_apenas_lider_pode_registrar_projeto(self):
        with self.app.app_context():
            service = ProjetoService(
                EquipeRepository(),
                ProjetoRepository(),
                HackathonRepository(),
            )

            with self.assertRaises(BusinessRuleError):
                service.registrar_projeto(
                    self.equipe.id,
                    "Projeto indevido",
                    "Tentativa de outro participante.",
                    "Teste",
                    self.segundo_participante.id,
                )

    def test_avaliacao_exige_comentario(self):
        with self.app.app_context():
            usuario_service = UsuarioService(UsuarioRepository())
            segundo_jurado = usuario_service.cadastrar_colaborador(
                "Segundo Jurado",
                "jurado2@teste.com",
                "12345678",
                "JURADO",
            )
            HackathonService(
                HackathonRepository(),
                UsuarioRepository(),
            ).associar_jurado(
                self.hackathon.id,
                segundo_jurado.id,
                self.organizador.id,
            )

            service = AvaliacaoService(
                UsuarioRepository(),
                ProjetoRepository(),
                AvaliacaoRepository(),
                HackathonRepository(),
            )

            with self.assertRaises(BusinessRuleError):
                service.registrar_avaliacao(
                    segundo_jurado.id,
                    self.projeto.id,
                    9,
                    "   ",
                )

    def test_autorizacao_e_contexto_da_avaliacao(self):
        client = self.app.test_client()

        response = client.get("/equipes/nova")
        self.assertEqual(response.status_code, 302)
        self.assertIn("/auth/login", response.location)

        client.post(
            "/auth/login",
            data={"email": "jurado@teste.com", "senha": "12345678"},
        )
        response = client.get("/avaliacoes/nova")

        self.assertEqual(response.status_code, 200)
        self.assertIn("Hackathon UFPR".encode(), response.data)
        self.assertIn("EcoTrack".encode(), response.data)
        self.assertNotIn(b'name="jurado_id"', response.data)

        response = client.get(
            f"/avaliacoes/?hackathon_id={self.hackathon.id}&projeto_id={self.projeto.id}"
        )
        self.assertIn("Hackathon UFPR".encode(), response.data)
        self.assertIn("Equipe Alpha".encode(), response.data)
        self.assertIn("João Jurado".encode(), response.data)

    def test_participante_pode_consultar_mentorias_da_propria_equipe(self):
        client = self.app.test_client()

        client.post(
            "/auth/login",
            data={
                "email": "ana@teste.com",
                "senha": "12345678",
            },
        )

        response = client.get(
            f"/mentorias/?equipe_id={self.equipe.id}"
        )

        self.assertEqual(response.status_code, 200)

        self.assertIn(
            "Hackathon UFPR".encode(),
            response.data,
        )

        self.assertIn(
            "Equipe Alpha".encode(),
            response.data,
        )

        self.assertIn(
            "Maria Mentor".encode(),
            response.data,
        )

        self.assertIn(
            "Validar a proposta com usuários.".encode(),
            response.data,
        )


class ComandoOrganizadorTestCase(unittest.TestCase):
    def test_comando_criar_organizador(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            database_path = Path(temp_dir) / "cli.sqlite3"
            app = create_app(
                {
                    "TESTING": True,
                    "DATABASE": str(database_path),
                    "SECRET_KEY": "test-secret-key",
                }
            )

            with app.app_context():
                init_db()

            runner = app.test_cli_runner()
            result = runner.invoke(
                args=[
                    "criar-organizador",
                    "--nome",
                    "Arthur",
                    "--email",
                    "arthur@teste.com",
                    "--senha",
                    "12345678",
                ]
            )

            self.assertEqual(result.exit_code, 0, result.output)
            self.assertIn("criado com sucesso", result.output)

            with app.app_context():
                usuario = UsuarioRepository().buscar_por_email("arthur@teste.com")
                self.assertIsNotNone(usuario)
                self.assertEqual(usuario.papel.value, "ORGANIZADOR")


if __name__ == "__main__":
    unittest.main()
