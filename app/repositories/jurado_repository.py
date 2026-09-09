from app.database.connection import get_db
from app.domain.models import Jurado


class JuradoRepository:
    def buscar_por_id(self, jurado_id: int):
        db = get_db()

        row = db.execute(
            """
            SELECT id, nome, email
            FROM jurados
            WHERE id = ?
            """,
            (jurado_id,),
        ).fetchone()

        if row is None:
            return None

        return Jurado(
            id=row["id"],
            nome=row["nome"],
            email=row["email"],
        )

    def listar_todos(self):
        db = get_db()

        rows = db.execute(
            """
            SELECT id, nome, email
            FROM jurados
            ORDER BY nome
            """
        ).fetchall()

        return [
            Jurado(
                id=row["id"],
                nome=row["nome"],
                email=row["email"],
            )
            for row in rows
        ]

    def salvar(self, jurado: Jurado):
        db = get_db()

        cursor = db.execute(
            """
            INSERT INTO jurados (nome, email)
            VALUES (?, ?)
            """,
            (jurado.nome, jurado.email),
        )

        db.commit()

        jurado.id = cursor.lastrowid

        return jurado