DROP TABLE IF EXISTS avaliacoes;
DROP TABLE IF EXISTS mentorias;
DROP TABLE IF EXISTS projetos;
DROP TABLE IF EXISTS equipe_participantes;
DROP TABLE IF EXISTS equipes;
DROP TABLE IF EXISTS hackathon_jurados;
DROP TABLE IF EXISTS hackathon_mentores;
DROP TABLE IF EXISTS hackathons;

-- Tabelas da primeira versão do projeto. Estes DROP permitem atualizar um banco
-- local antigo sem deixar resíduos do modelo anterior.
DROP TABLE IF EXISTS participantes;
DROP TABLE IF EXISTS jurados;
DROP TABLE IF EXISTS mentores;

DROP TABLE IF EXISTS usuarios;


CREATE TABLE usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    senha_hash TEXT NOT NULL,
    papel TEXT NOT NULL
        CHECK (papel IN ('ORGANIZADOR', 'PARTICIPANTE', 'JURADO', 'MENTOR'))
);


CREATE TABLE hackathons (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    data_inicio TEXT NOT NULL,
    data_fim TEXT NOT NULL,
    max_equipes INTEGER NOT NULL CHECK (max_equipes > 0),
    organizador_id INTEGER NOT NULL,

    FOREIGN KEY (organizador_id) REFERENCES usuarios(id)
);


CREATE TABLE hackathon_jurados (
    hackathon_id INTEGER NOT NULL,
    jurado_id INTEGER NOT NULL,

    PRIMARY KEY (hackathon_id, jurado_id),
    FOREIGN KEY (hackathon_id) REFERENCES hackathons(id) ON DELETE CASCADE,
    FOREIGN KEY (jurado_id) REFERENCES usuarios(id)
);


CREATE TABLE hackathon_mentores (
    hackathon_id INTEGER NOT NULL,
    mentor_id INTEGER NOT NULL,

    PRIMARY KEY (hackathon_id, mentor_id),
    FOREIGN KEY (hackathon_id) REFERENCES hackathons(id) ON DELETE CASCADE,
    FOREIGN KEY (mentor_id) REFERENCES usuarios(id)
);


CREATE TABLE equipes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    hackathon_id INTEGER NOT NULL,
    lider_id INTEGER NOT NULL,

    FOREIGN KEY (hackathon_id) REFERENCES hackathons(id) ON DELETE CASCADE,
    FOREIGN KEY (lider_id) REFERENCES usuarios(id)
);


CREATE TABLE equipe_participantes (
    equipe_id INTEGER NOT NULL,
    usuario_id INTEGER NOT NULL,

    PRIMARY KEY (equipe_id, usuario_id),
    FOREIGN KEY (equipe_id) REFERENCES equipes(id) ON DELETE CASCADE,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
);


CREATE TABLE projetos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titulo TEXT NOT NULL,
    descricao TEXT NOT NULL,
    area_tematica TEXT NOT NULL,
    equipe_id INTEGER NOT NULL UNIQUE,

    FOREIGN KEY (equipe_id) REFERENCES equipes(id) ON DELETE CASCADE
);


CREATE TABLE mentorias (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    comentario TEXT NOT NULL,
    mentor_id INTEGER NOT NULL,
    equipe_id INTEGER NOT NULL,

    FOREIGN KEY (mentor_id) REFERENCES usuarios(id),
    FOREIGN KEY (equipe_id) REFERENCES equipes(id) ON DELETE CASCADE
);


CREATE TABLE avaliacoes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nota REAL NOT NULL CHECK (nota >= 0 AND nota <= 10),
    comentario TEXT NOT NULL,
    jurado_id INTEGER NOT NULL,
    projeto_id INTEGER NOT NULL,

    UNIQUE (jurado_id, projeto_id),
    FOREIGN KEY (jurado_id) REFERENCES usuarios(id),
    FOREIGN KEY (projeto_id) REFERENCES projetos(id) ON DELETE CASCADE
);


CREATE INDEX idx_equipes_hackathon ON equipes(hackathon_id);
CREATE INDEX idx_equipe_participantes_usuario ON equipe_participantes(usuario_id);
CREATE INDEX idx_projetos_equipe ON projetos(equipe_id);
CREATE INDEX idx_avaliacoes_projeto ON avaliacoes(projeto_id);
CREATE INDEX idx_mentorias_equipe ON mentorias(equipe_id);
