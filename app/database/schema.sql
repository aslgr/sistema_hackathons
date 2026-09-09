DROP TABLE IF EXISTS avaliacoes;
DROP TABLE IF EXISTS mentorias;
DROP TABLE IF EXISTS projetos;
DROP TABLE IF EXISTS equipe_participantes;
DROP TABLE IF EXISTS equipes;
DROP TABLE IF EXISTS jurados;
DROP TABLE IF EXISTS mentores;
DROP TABLE IF EXISTS participantes;
DROP TABLE IF EXISTS hackathons;


CREATE TABLE hackathons (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    data_inicio TEXT NOT NULL,
    data_fim TEXT NOT NULL,
    max_equipes INTEGER NOT NULL
);


CREATE TABLE participantes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    email TEXT NOT NULL
);


CREATE TABLE equipes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,

    hackathon_id INTEGER NOT NULL,

    FOREIGN KEY (hackathon_id)
        REFERENCES hackathons(id)
        ON DELETE CASCADE
);


CREATE TABLE equipe_participantes (
    equipe_id INTEGER NOT NULL,
    participante_id INTEGER NOT NULL,

    PRIMARY KEY (equipe_id, participante_id),

    FOREIGN KEY (equipe_id)
        REFERENCES equipes(id)
        ON DELETE CASCADE,

    FOREIGN KEY (participante_id)
        REFERENCES participantes(id)
        ON DELETE CASCADE
);


CREATE TABLE projetos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titulo TEXT NOT NULL,
    descricao TEXT NOT NULL,
    area_tematica TEXT NOT NULL,

    equipe_id INTEGER NOT NULL UNIQUE,

    FOREIGN KEY (equipe_id)
        REFERENCES equipes(id)
        ON DELETE CASCADE
);


CREATE TABLE mentores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    email TEXT NOT NULL
);


CREATE TABLE mentorias (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    comentario TEXT NOT NULL,

    mentor_id INTEGER NOT NULL,
    equipe_id INTEGER NOT NULL,

    FOREIGN KEY (mentor_id)
        REFERENCES mentores(id),

    FOREIGN KEY (equipe_id)
        REFERENCES equipes(id)
        ON DELETE CASCADE
);


CREATE TABLE jurados (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    email TEXT NOT NULL
);


CREATE TABLE avaliacoes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nota REAL NOT NULL CHECK (nota >= 0 AND nota <= 10),
    comentario TEXT NOT NULL,

    jurado_id INTEGER NOT NULL,
    projeto_id INTEGER NOT NULL,

    UNIQUE (jurado_id, projeto_id),

    FOREIGN KEY (jurado_id)
        REFERENCES jurados(id),

    FOREIGN KEY (projeto_id)
        REFERENCES projetos(id)
        ON DELETE CASCADE
);