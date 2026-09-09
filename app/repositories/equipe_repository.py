from app.database.connection import get_db
from app.domain.models import Equipe, Participante


class EquipeRepository:
    def contar_por_hackathon(self, hackathon_id: int):
        db = get_db()

        row = db.execute(
            """
            SELECT COUNT(*) AS quantidade
            FROM equipes
            WHERE hackathon_id = ?
            """,
            (hackathon_id,),
        ).fetchone()

        return row["quantidade"]

    def buscar_por_participante_e_hackathon(
        self,
        participante_id: int,
        hackathon_id: int,
    ):
        db = get_db()

        row = db.execute(
            """
            SELECT e.id
            FROM equipes e
            JOIN equipe_participantes ep
                ON ep.equipe_id = e.id
            WHERE ep.participante_id = ?
              AND e.hackathon_id = ?
            """,
            (participante_id, hackathon_id),
        ).fetchone()

        return row

    def salvar(self, equipe: Equipe):
        db = get_db()

        cursor = db.execute(
            """
            INSERT INTO equipes (nome, hackathon_id)
            VALUES (?, ?)
            """,
            (
                equipe.nome,
                equipe.hackathon.id,
            ),
        )

        equipe.id = cursor.lastrowid

        for participante in equipe.participantes:
            db.execute(
                """
                INSERT INTO equipe_participantes (
                    equipe_id,
                    participante_id
                )
                VALUES (?, ?)
                """,
                (
                    equipe.id,
                    participante.id,
                ),
            )

        db.commit()

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
                h.max_equipes
            FROM equipes e
            JOIN hackathons h
                ON h.id = e.hackathon_id
            WHERE e.id = ?
            """,
            (equipe_id,),
        ).fetchone()

        if row is None:
            return None

        from datetime import date
        from app.domain.models import Hackathon

        hackathon = Hackathon(
            id=row["hackathon_id"],
            nome=row["hackathon_nome"],
            data_inicio=date.fromisoformat(row["data_inicio"]),
            data_fim=date.fromisoformat(row["data_fim"]),
            max_equipes=row["max_equipes"],
        )

        participantes_rows = db.execute(
            """
            SELECT p.id, p.nome, p.email
            FROM participantes p
            JOIN equipe_participantes ep
                ON ep.participante_id = p.id
            WHERE ep.equipe_id = ?
            """,
            (equipe_id,),
        ).fetchall()

        participantes = [
            Participante(
                id=p["id"],
                nome=p["nome"],
                email=p["email"],
            )
            for p in participantes_rows
        ]

        return Equipe(
            id=row["equipe_id"],
            nome=row["equipe_nome"],
            hackathon=hackathon,
            participantes=participantes,
        )


    def listar_todas(self):
        db = get_db()

        rows = db.execute(
            """
            SELECT
                e.id,
                e.nome,
                e.hackathon_id,
                h.nome AS hackathon_nome
            FROM equipes e
            JOIN hackathons h
                ON h.id = e.hackathon_id
            ORDER BY h.nome, e.nome
            """
        ).fetchall()

        return rows


    def adicionar_participante(
        self,
        equipe_id: int,
        participante_id: int,
    ):
        db = get_db()

        db.execute(
            """
            INSERT INTO equipe_participantes (
                equipe_id,
                participante_id
            )
            VALUES (?, ?)
            """,
            (
                equipe_id,
                participante_id,
            ),
        )

        db.commit()