import os
import secrets
from pathlib import Path


def obter_secret_key(instance_path: str) -> str:
    """Retorna a chave usada pelo Flask para assinar a sessão.

    Em ambientes publicados, a chave pode ser fornecida pela variável de ambiente
    SECRET_KEY. No desenvolvimento local, uma chave aleatória é gerada uma única
    vez e armazenada dentro de instance/, diretório ignorado pelo Git.
    """
    secret_key = os.getenv("SECRET_KEY")
    if secret_key:
        return secret_key

    secret_path = Path(instance_path) / ".secret_key"

    if secret_path.exists():
        saved_key = secret_path.read_text(encoding="utf-8").strip()
        if saved_key:
            return saved_key

    secret_key = secrets.token_hex(32)
    secret_path.write_text(secret_key, encoding="utf-8")

    try:
        secret_path.chmod(0o600)
    except OSError:
        pass

    return secret_key
