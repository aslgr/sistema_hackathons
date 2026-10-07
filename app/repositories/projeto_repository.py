from app.database.connection import get_db
from app.domain.models import Projeto
from app.repositories.equipe_repository import EquipeRepository


class ProjetoRepository:
    def __init__(self):
        self.equipe_repository = EquipeRepository()

    def buscar_por_id(self, projeto_id: int):
        row = get_db().execute(
            """
            SELECT id, titulo, descricao, area_tematica, equipe_id
            FROM projetos
            WHERE id = ?
            """,
            (projeto_id,),
        ).fetchone()

        if row is None:
            return None

        return self._criar_projeto(row)

    def listar_todos(self):
        rows = get_db().execute(
            """
            SELECT id, titulo, descricao, area_tematica, equipe_id
            FROM projetos
            ORDER BY titulo
            """
        ).fetchall()
        return [self._criar_projeto(row) for row in rows]

    def listar_por_hackathon(self, hackathon_id: int):
        rows = get_db().execute(
            """
            SELECT p.id, p.titulo, p.descricao, p.area_tematica, p.equipe_id
            FROM projetos p
            JOIN equipes e ON e.id = p.equipe_id
            WHERE e.hackathon_id = ?
            ORDER BY p.titulo
            """,
            (hackathon_id,),
        ).fetchall()
        return [self._criar_projeto(row) for row in rows]

    def listar_para_jurado(self, jurado_id: int):
        rows = get_db().execute(
            """
            SELECT p.id, p.titulo, p.descricao, p.area_tematica, p.equipe_id
            FROM projetos p
            JOIN equipes e ON e.id = p.equipe_id
            JOIN hackathon_jurados hj ON hj.hackathon_id = e.hackathon_id
            WHERE hj.jurado_id = ?
            ORDER BY e.hackathon_id, p.titulo
            """,
            (jurado_id,),
        ).fetchall()
        return [self._criar_projeto(row) for row in rows]

    def existe_para_equipe(self, equipe_id: int) -> bool:
        row = get_db().execute(
            """
            SELECT 1
            FROM projetos
            WHERE equipe_id = ?
            """,
            (equipe_id,),
        ).fetchone()
        return row is not None

    def salvar(self, projeto: Projeto):
        db = get_db()
        cursor = db.execute(
            """
            INSERT INTO projetos (titulo, descricao, area_tematica, equipe_id)
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

    def _criar_projeto(self, row):
        equipe = self.equipe_repository.buscar_por_id(row["equipe_id"])
        return Projeto(
            id=row["id"],
            titulo=row["titulo"],
            descricao=row["descricao"],
            area_tematica=row["area_tematica"],
            equipe=equipe,
        )
