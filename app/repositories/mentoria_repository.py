from app.database.connection import get_db
from app.domain.models import Mentoria


class MentoriaRepository:
    def salvar(self, mentoria: Mentoria):
        db = get_db()

        cursor = db.execute(
            """
            INSERT INTO mentorias (
                comentario,
                mentor_id,
                equipe_id
            )
            VALUES (?, ?, ?)
            """,
            (
                mentoria.comentario,
                mentoria.mentor.id,
                mentoria.equipe.id,
            ),
        )

        db.commit()

        mentoria.id = cursor.lastrowid

        return mentoria