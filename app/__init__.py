from pathlib import Path

from flask import Flask, render_template


def create_app():
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(
        SECRET_KEY="dev",
        DATABASE=str(Path(app.instance_path) / "hackathons.sqlite3"),
    )

    Path(app.instance_path).mkdir(parents=True, exist_ok=True)

    from app.database.connection import init_app as init_database

    init_database(app)

    from app.routes.hackathons import hackathons_bp
    from app.routes.participantes import participantes_bp
    from app.routes.equipes import equipes_bp
    from app.routes.projetos import projetos_bp
    from app.routes.avaliacoes import avaliacoes_bp
    from app.routes.classificacao import classificacao_bp
    from app.routes.jurados import jurados_bp

    app.register_blueprint(hackathons_bp)
    app.register_blueprint(participantes_bp)
    app.register_blueprint(equipes_bp)
    app.register_blueprint(projetos_bp)
    app.register_blueprint(avaliacoes_bp)
    app.register_blueprint(classificacao_bp)
    app.register_blueprint(jurados_bp)

    @app.get("/")
    def index():
        return render_template("index.html")

    return app