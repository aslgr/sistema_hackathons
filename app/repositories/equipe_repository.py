from datetime import date

from app.database.connection import get_db
from app.domain.models import Equipe, Hackathon, PapelUsuario, Usuario


class EquipeRepository:
    def buscar_por_id(self, equipe_id: int):
        db = get_db()
        row = db.execute(
            """
            SELECT
                e.id AS equipe_id,
                e.nome AS equipe_nome,
                h.id AS hackathon_id,
                h.nome AS hackathon_nome,
                h.data_inicio,
                h.data_fim,
                h.max_equipes,
                org.id AS organizador_id,
                org.nome AS organizador_nome,
                org.email AS organizador_email,
                org.senha_hash AS organizador_senha_hash,
                org.papel AS organizador_papel,
                l.id AS lider_id,
                l.nome AS lider_nome,
                l.email AS lider_email,
                l.senha_hash AS lider_senha_hash,
                l.papel AS lider_papel
            FROM equipes e
            JOIN hackathons h ON h.id = e.hackathon_id
            JOIN usuarios org ON org.id = h.organizador_id
            JOIN usuarios l ON l.id = e.lider_id
            WHERE e.id = ?
            """,
            (equipe_id,),
        ).fetchone()

        if row is None:
            return None

        participantes_rows = db.execute(
            """
            SELECT u.id, u.nome, u.email, u.senha_hash, u.papel
            FROM usuarios u
            JOIN equipe_participantes ep ON ep.usuario_id = u.id
            WHERE ep.equipe_id = ?
            ORDER BY u.nome
            """,
            (equipe_id,),
        ).fetchall()

        participantes = [
            Usuario(
                id=participante["id"],
                nome=participante["nome"],
                email=participante["email"],
                senha_hash=participante["senha_hash"],
                papel=PapelUsuario(participante["papel"]),
            )
            for participante in participantes_rows
        ]

        return Equipe(
            id=row["equipe_id"],
            nome=row["equipe_nome"],
            hackathon=self._criar_hackathon(row),
            lider=self._criar_lider(row),
            participantes=participantes,
        )

    def listar_por_hackathon(self, hackathon_id: int):
        return get_db().execute(
            """
            SELECT
                e.id,
                e.nome,
                h.nome AS hackathon_nome,
                l.nome AS lider_nome,
                COUNT(ep.usuario_id) AS quantidade_participantes
            FROM equipes e
            JOIN hackathons h ON h.id = e.hackathon_id
            JOIN usuarios l ON l.id = e.lider_id
            LEFT JOIN equipe_participantes ep ON ep.equipe_id = e.id
            WHERE e.hackathon_id = ?
            GROUP BY e.id, e.nome, h.nome, l.nome
            ORDER BY e.nome
            """,
            (hackathon_id,),
        ).fetchall()

    def listar_por_lider(self, lider_id: int):
        return get_db().execute(
            """
            SELECT e.id, e.nome, h.nome AS hackathon_nome
            FROM equipes e
            JOIN hackathons h ON h.id = e.hackathon_id
            WHERE e.lider_id = ?
            ORDER BY h.nome, e.nome
            """,
            (lider_id,),
        ).fetchall()

    def listar_para_mentor(self, mentor_id: int):
        return get_db().execute(
            """
            SELECT e.id, e.nome, h.nome AS hackathon_nome
            FROM equipes e
            JOIN hackathons h ON h.id = e.hackathon_id
            JOIN hackathon_mentores hm ON hm.hackathon_id = h.id
            WHERE hm.mentor_id = ?
            ORDER BY h.nome, e.nome
            """,
            (mentor_id,),
        ).fetchall()

    def contar_por_hackathon(self, hackathon_id: int) -> int:
        row = get_db().execute(
            """
            SELECT COUNT(*) AS quantidade
            FROM equipes
            WHERE hackathon_id = ?
            """,
            (hackathon_id,),
        ).fetchone()
        return row["quantidade"]

    def participante_esta_em_hackathon(self, usuario_id: int, hackathon_id: int) -> bool:
        row = get_db().execute(
            """
            SELECT 1
            FROM equipes e
            JOIN equipe_participantes ep ON ep.equipe_id = e.id
            WHERE ep.usuario_id = ? AND e.hackathon_id = ?
            """,
            (usuario_id, hackathon_id),
        ).fetchone()
        return row is not None

    def listar_por_participante(self, usuario_id: int):
        return get_db().execute(
            """
            SELECT
                e.id,
                e.nome,
                h.nome AS hackathon_nome
            FROM equipes e
            JOIN hackathons h ON h.id = e.hackathon_id
            JOIN equipe_participantes ep ON ep.equipe_id = e.id
            WHERE ep.usuario_id = ?
            ORDER BY h.nome, e.nome
            """,
            (usuario_id,),
        ).fetchall()

    def participante_esta_na_equipe(self, usuario_id: int, equipe_id: int) -> bool:
        row = get_db().execute(
            """
            SELECT 1
            FROM equipe_participantes
            WHERE usuario_id = ?
            AND equipe_id = ?
            """,
            (usuario_id, equipe_id),
        ).fetchone()

        return row is not None

    def salvar(self, equipe: Equipe):
        db = get_db()
        cursor = db.execute(
            """
            INSERT INTO equipes (nome, hackathon_id, lider_id)
            VALUES (?, ?, ?)
            """,
            (equipe.nome, equipe.hackathon.id, equipe.lider.id),
        )
        equipe.id = cursor.lastrowid

        for participante in equipe.participantes:
            db.execute(
                """
                INSERT INTO equipe_participantes (equipe_id, usuario_id)
                VALUES (?, ?)
                """,
                (equipe.id, participante.id),
            )

        db.commit()
        return equipe

    def adicionar_participante(self, equipe_id: int, usuario_id: int):
        db = get_db()
        db.execute(
            """
            INSERT INTO equipe_participantes (equipe_id, usuario_id)
            VALUES (?, ?)
            """,
            (equipe_id, usuario_id),
        )
        db.commit()

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
            id=row["hackathon_id"],
            nome=row["hackathon_nome"],
            data_inicio=date.fromisoformat(row["data_inicio"]),
            data_fim=date.fromisoformat(row["data_fim"]),
            max_equipes=row["max_equipes"],
            organizador=organizador,
        )

    @staticmethod
    def _criar_lider(row):
        return Usuario(
            id=row["lider_id"],
            nome=row["lider_nome"],
            email=row["lider_email"],
            senha_hash=row["lider_senha_hash"],
            papel=PapelUsuario(row["lider_papel"]),
        )
