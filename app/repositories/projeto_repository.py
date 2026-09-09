from app.database.connection import get_db
from app.domain.models import Projeto


class ProjetoRepository:
    def buscar_por_equipe(self, equipe_id: int):
        db = get_db()

        row = db.execute(
            """
            SELECT id
            FROM projetos
            WHERE equipe_id = ?
            """,
            (equipe_id,),
        ).fetchone()

        return row

    def salvar(self, projeto: Projeto):
        db = get_db()

        cursor = db.execute(
            """
            INSERT INTO projetos (
                titulo,
                descricao,
                area_tematica,
                equipe_id
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                projeto.titulo,
                projeto.descricao,
                projeto.area_tematica,
                projeto.equipe.id,
            ),
        )

        db.commit()

        projeto.id = cursor.lastrowid

        return projeto