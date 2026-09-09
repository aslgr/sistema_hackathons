from app.database.connection import get_db
from app.domain.models import Mentor


class MentorRepository:
    def buscar_por_id(self, mentor_id: int):
        db = get_db()

        row = db.execute(
            """
            SELECT id, nome, email
            FROM mentores
            WHERE id = ?
            """,
            (mentor_id,),
        ).fetchone()

        if row is None:
            return None

        return Mentor(
            id=row["id"],
            nome=row["nome"],
            email=row["email"],
        )

    def listar_todos(self):
        db = get_db()

        rows = db.execute(
            """
            SELECT id, nome, email
            FROM mentores
            ORDER BY nome
            """
        ).fetchall()

        return [
            Mentor(
                id=row["id"],
                nome=row["nome"],
                email=row["email"],
            )
            for row in rows
        ]

    def salvar(self, mentor: Mentor):
        db = get_db()

        cursor = db.execute(
            """
            INSERT INTO mentores (nome, email)
            VALUES (?, ?)
            """,
            (mentor.nome, mentor.email),
        )

        db.commit()

        mentor.id = cursor.lastrowid

        return mentor