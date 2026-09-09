from datetime import date

from app.database.connection import get_db
from app.domain.models import Hackathon


class HackathonRepository:
    def buscar_por_id(self, hackathon_id: int):
        db = get_db()

        row = db.execute(
            """
            SELECT id, nome, data_inicio, data_fim, max_equipes
            FROM hackathons
            WHERE id = ?
            """,
            (hackathon_id,),
        ).fetchone()

        if row is None:
            return None

        return Hackathon(
            id=row["id"],
            nome=row["nome"],
            data_inicio=date.fromisoformat(row["data_inicio"]),
            data_fim=date.fromisoformat(row["data_fim"]),
            max_equipes=row["max_equipes"],
        )

    def listar_todos(self):
        db = get_db()

        rows = db.execute(
            """
            SELECT id, nome, data_inicio, data_fim, max_equipes
            FROM hackathons
            ORDER BY data_inicio
            """
        ).fetchall()

        return [
            Hackathon(
                id=row["id"],
                nome=row["nome"],
                data_inicio=date.fromisoformat(row["data_inicio"]),
                data_fim=date.fromisoformat(row["data_fim"]),
                max_equipes=row["max_equipes"],
            )
            for row in rows
        ]

    def salvar(self, hackathon: Hackathon):
        db = get_db()

        cursor = db.execute(
            """
            INSERT INTO hackathons (
                nome,
                data_inicio,
                data_fim,
                max_equipes
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                hackathon.nome,
                hackathon.data_inicio.isoformat(),
                hackathon.data_fim.isoformat(),
                hackathon.max_equipes,
            ),
        )

        db.commit()

        hackathon.id = cursor.lastrowid

        return hackathon