from datetime import date

from app.database.connection import get_db
from app.domain.models import Hackathon, PapelUsuario, Usuario


class HackathonRepository:
    _SELECT_BASE = """
        SELECT
            h.id,
            h.nome,
            h.data_inicio,
            h.data_fim,
            h.max_equipes,
            u.id AS organizador_id,
            u.nome AS organizador_nome,
            u.email AS organizador_email,
            u.senha_hash AS organizador_senha_hash,
            u.papel AS organizador_papel
        FROM hackathons h
        JOIN usuarios u ON u.id = h.organizador_id
    """

    def buscar_por_id(self, hackathon_id: int):
        row = get_db().execute(
            f"{self._SELECT_BASE} WHERE h.id = ?",
            (hackathon_id,),
        ).fetchone()

        return self._criar_hackathon(row) if row else None

    def listar_todos(self):
        rows = get_db().execute(
            f"{self._SELECT_BASE} ORDER BY h.data_inicio, h.nome"
        ).fetchall()
        return [self._criar_hackathon(row) for row in rows]

    def listar_por_organizador(self, organizador_id: int):
        rows = get_db().execute(
            f"""
            {self._SELECT_BASE}
            WHERE h.organizador_id = ?
            ORDER BY h.data_inicio, h.nome
            """,
            (organizador_id,),
        ).fetchall()
        return [self._criar_hackathon(row) for row in rows]

    def salvar(self, hackathon: Hackathon):
        db = get_db()
        cursor = db.execute(
            """
            INSERT INTO hackathons (
                nome,
                data_inicio,
                data_fim,
                max_equipes,
                organizador_id
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                hackathon.nome,
                hackathon.data_inicio.isoformat(),
                hackathon.data_fim.isoformat(),
                hackathon.max_equipes,
                hackathon.organizador.id,
            ),
        )
        db.commit()

        hackathon.id = cursor.lastrowid
        return hackathon

    def associar_jurado(self, hackathon_id: int, jurado_id: int):
        db = get_db()
        db.execute(
            """
            INSERT INTO hackathon_jurados (hackathon_id, jurado_id)
            VALUES (?, ?)
            """,
            (hackathon_id, jurado_id),
        )
        db.commit()

    def associar_mentor(self, hackathon_id: int, mentor_id: int):
        db = get_db()
        db.execute(
            """
            INSERT INTO hackathon_mentores (hackathon_id, mentor_id)
            VALUES (?, ?)
            """,
            (hackathon_id, mentor_id),
        )
        db.commit()

    def jurado_associado(self, hackathon_id: int, jurado_id: int) -> bool:
        row = get_db().execute(
            """
            SELECT 1
            FROM hackathon_jurados
            WHERE hackathon_id = ? AND jurado_id = ?
            """,
            (hackathon_id, jurado_id),
        ).fetchone()
        return row is not None

    def mentor_associado(self, hackathon_id: int, mentor_id: int) -> bool:
        row = get_db().execute(
            """
            SELECT 1
            FROM hackathon_mentores
            WHERE hackathon_id = ? AND mentor_id = ?
            """,
            (hackathon_id, mentor_id),
        ).fetchone()
        return row is not None

    @staticmethod
    def _criar_hackathon(row):
        organizador = Usuario(
            id=row["organizador_id"],
            nome=row["organizador_nome"],
            email=row["organizador_email"],
            senha_hash=row["organizador_senha_hash"],
            papel=PapelUsuario(row["organizador_papel"]),
        )

        return Hackathon(
            id=row["id"],
            nome=row["nome"],
            data_inicio=date.fromisoformat(row["data_inicio"]),
            data_fim=date.fromisoformat(row["data_fim"]),
            max_equipes=row["max_equipes"],
            organizador=organizador,
        )
