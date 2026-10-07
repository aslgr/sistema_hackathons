from pathlib import Path

from flask import Flask, render_template

from app.config import obter_secret_key


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    instance_path = Path(app.instance_path)
    instance_path.mkdir(parents=True, exist_ok=True)

    secret_key = (
        test_config["SECRET_KEY"]
        if test_config is not None and "SECRET_KEY" in test_config
        else obter_secret_key(app.instance_path)
    )

    app.config.from_mapping(
        DATABASE=str(instance_path / "hackathons.sqlite3"),
        SECRET_KEY=secret_key,
    )

    if test_config is not None:
        app.config.update(test_config)

    from app.cli import init_app as init_cli
    from app.database.connection import init_app as init_database

    init_database(app)
    init_cli(app)

    from app.routes.auth import auth_bp
    from app.routes.avaliacoes import avaliacoes_bp
    from app.routes.classificacao import classificacao_bp
    from app.routes.equipes import equipes_bp
    from app.routes.hackathons import hackathons_bp
    from app.routes.mentorias import mentorias_bp
    from app.routes.projetos import projetos_bp
    from app.routes.usuarios import usuarios_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(hackathons_bp)
    app.register_blueprint(usuarios_bp)
    app.register_blueprint(equipes_bp)
    app.register_blueprint(projetos_bp)
    app.register_blueprint(mentorias_bp)
    app.register_blueprint(avaliacoes_bp)
    app.register_blueprint(classificacao_bp)

    @app.get("/")
    def index():
        return render_template("index.html")

    return app
