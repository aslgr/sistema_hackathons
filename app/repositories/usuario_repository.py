from app.database.connection import get_db
from app.domain.models import PapelUsuario, Usuario


class UsuarioRepository:
    def buscar_por_id(self, usuario_id: int):
        row = get_db().execute(
            """
            SELECT id, nome, email, senha_hash, papel
            FROM usuarios
            WHERE id = ?
            """,
            (usuario_id,),
        ).fetchone()

        return self._criar_usuario(row) if row else None

    def buscar_por_email(self, email: str):
        row = get_db().execute(
            """
            SELECT id, nome, email, senha_hash, papel
            FROM usuarios
            WHERE email = ?
            """,
            (email,),
        ).fetchone()

        return self._criar_usuario(row) if row else None

    def listar_por_papel(self, papel: PapelUsuario):
        rows = get_db().execute(
            """
            SELECT id, nome, email, senha_hash, papel
            FROM usuarios
            WHERE papel = ?
            ORDER BY nome
            """,
            (papel.value,),
        ).fetchall()

        return [self._criar_usuario(row) for row in rows]

    def salvar(self, usuario: Usuario):
        db = get_db()
        cursor = db.execute(
            """
            INSERT INTO usuarios (nome, email, senha_hash, papel)
            VALUES (?, ?, ?, ?)
            """,
            (
                usuario.nome,
                usuario.email,
                usuario.senha_hash,
                usuario.papel.value,
            ),
        )
        db.commit()

        usuario.id = cursor.lastrowid
        return usuario

    @staticmethod
    def _criar_usuario(row):
        return Usuario(
            id=row["id"],
            nome=row["nome"],
            email=row["email"],
            senha_hash=row["senha_hash"],
            papel=PapelUsuario(row["papel"]),
        )
