from app.database.connection import get_db
from app.domain.models import Avaliacao


class AvaliacaoRepository:
    def buscar_por_jurado_e_projeto(self, jurado_id: int, projeto_id: int):
        return get_db().execute(
            """
            SELECT id
            FROM avaliacoes
            WHERE jurado_id = ? AND projeto_id = ?
            """,
            (jurado_id, projeto_id),
        ).fetchone()

    def listar_por_hackathon(self, hackathon_id: int):
        return get_db().execute(
            """
            SELECT a.id, a.projeto_id, a.jurado_id, a.nota, a.comentario
            FROM avaliacoes a
            JOIN projetos p ON p.id = a.projeto_id
            JOIN equipes e ON e.id = p.equipe_id
            WHERE e.hackathon_id = ?
            """,
            (hackathon_id,),
        ).fetchall()

    def listar_por_projeto(self, projeto_id: int):
        return get_db().execute(
            """
            SELECT a.id, a.nota, a.comentario, u.nome AS jurado_nome
            FROM avaliacoes a
            JOIN usuarios u ON u.id = a.jurado_id
            WHERE a.projeto_id = ?
            ORDER BY u.nome
            """,
            (projeto_id,),
        ).fetchall()

    def salvar(self, avaliacao: Avaliacao):
        db = get_db()
        cursor = db.execute(
            """
            INSERT INTO avaliacoes (nota, comentario, jurado_id, projeto_id)
            VALUES (?, ?, ?, ?)
            """,
            (
                avaliacao.nota,
                avaliacao.comentario,
                avaliacao.jurado.id,
                avaliacao.projeto.id,
            ),
        )
        db.commit()

        avaliacao.id = cursor.lastrowid
        return avaliacao
