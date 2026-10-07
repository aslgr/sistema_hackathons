from app.database.connection import get_db
from app.domain.models import Mentoria


class MentoriaRepository:
    def listar_por_equipe(self, equipe_id: int):
        return get_db().execute(
            """
            SELECT
                m.id,
                m.comentario,
                u.nome AS mentor_nome
            FROM mentorias m
            JOIN usuarios u ON u.id = m.mentor_id
            WHERE m.equipe_id = ?
            ORDER BY m.id DESC
            """,
            (equipe_id,),
        ).fetchall()
    
    def salvar(self, mentoria: Mentoria):
        db = get_db()
        cursor = db.execute(
            """
            INSERT INTO mentorias (comentario, mentor_id, equipe_id)
            VALUES (?, ?, ?)
            """,
            (mentoria.comentario, mentoria.mentor.id, mentoria.equipe.id),
        )
        db.commit()

        mentoria.id = cursor.lastrowid
        return mentoria