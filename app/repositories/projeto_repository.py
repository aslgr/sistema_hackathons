from datetime import date

from app.database.connection import get_db
from app.domain.models import Equipe, Hackathon, Projeto


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

    def buscar_por_id(self, projeto_id: int):
        db = get_db()

        row = db.execute(
            """
            SELECT
                p.id AS projeto_id,
                p.titulo,
                p.descricao,
                p.area_tematica,

                e.id AS equipe_id,
                e.nome AS equipe_nome,

                h.id AS hackathon_id,
                h.nome AS hackathon_nome,
                h.data_inicio,
                h.data_fim,
                h.max_equipes

            FROM projetos p

            JOIN equipes e
                ON e.id = p.equipe_id

            JOIN hackathons h
                ON h.id = e.hackathon_id

            WHERE p.id = ?
            """,
            (projeto_id,),
        ).fetchone()

        if row is None:
            return None

        hackathon = Hackathon(
            id=row["hackathon_id"],
            nome=row["hackathon_nome"],
            data_inicio=date.fromisoformat(row["data_inicio"]),
            data_fim=date.fromisoformat(row["data_fim"]),
            max_equipes=row["max_equipes"],
        )

        equipe = Equipe(
            id=row["equipe_id"],
            nome=row["equipe_nome"],
            hackathon=hackathon,
            participantes=[],
        )

        return Projeto(
            id=row["projeto_id"],
            titulo=row["titulo"],
            descricao=row["descricao"],
            area_tematica=row["area_tematica"],
            equipe=equipe,
        )

    def listar_todos(self):
        db = get_db()

        rows = db.execute(
            """
            SELECT id
            FROM projetos
            ORDER BY titulo
            """
        ).fetchall()

        return [
            self.buscar_por_id(row["id"])
            for row in rows
        ]

    def listar_por_hackathon(self, hackathon_id: int):
        db = get_db()

        rows = db.execute(
            """
            SELECT p.id
            FROM projetos p

            JOIN equipes e
                ON e.id = p.equipe_id

            WHERE e.hackathon_id = ?

            ORDER BY p.titulo
            """,
            (hackathon_id,),
        ).fetchall()

        return [
            self.buscar_por_id(row["id"])
            for row in rows
        ]