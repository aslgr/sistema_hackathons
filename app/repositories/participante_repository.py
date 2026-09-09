from app.database.connection import get_db
from app.domain.models import Participante


class ParticipanteRepository:
    def buscar_por_id(self, participante_id: int):
        db = get_db()

        row = db.execute(
            """
            SELECT id, nome, email
            FROM participantes
            WHERE id = ?
            """,
            (participante_id,),
        ).fetchone()

        if row is None:
            return None

        return Participante(
            id=row["id"],
            nome=row["nome"],
            email=row["email"],
        )

    def salvar(self, participante: Participante):
        db = get_db()

        cursor = db.execute(
            """
            INSERT INTO participantes (nome, email)
            VALUES (?, ?)
            """,
            (participante.nome, participante.email),
        )

        db.commit()

        participante.id = cursor.lastrowid

        return participante

    def listar_todos(self):
        db = get_db()

        rows = db.execute(
            """
            SELECT id, nome, email
            FROM participantes
            ORDER BY nome
            """
        ).fetchall()

        return [
            Participante(
                id=row["id"],
                nome=row["nome"],
                email=row["email"],
            )
            for row in rows
        ]