from dataclasses import dataclass, field
from datetime import date


@dataclass
class Hackathon:
    id: int | None
    nome: str
    data_inicio: date
    data_fim: date
    max_equipes: int


@dataclass
class Participante:
    id: int | None
    nome: str
    email: str


@dataclass
class Equipe:
    id: int | None
    nome: str
    hackathon: Hackathon
    participantes: list[Participante] = field(default_factory=list)

    def adicionar_participante(self, participante: Participante):
        if participante not in self.participantes:
            self.participantes.append(participante)


@dataclass
class Projeto:
    id: int | None
    titulo: str
    descricao: str
    area_tematica: str
    equipe: Equipe


@dataclass
class Mentor:
    id: int | None
    nome: str
    email: str


@dataclass
class Mentoria:
    id: int | None
    mentor: Mentor
    equipe: Equipe
    comentario: str


@dataclass
class Jurado:
    id: int | None
    nome: str
    email: str


@dataclass
class Avaliacao:
    id: int | None
    jurado: Jurado
    projeto: Projeto
    nota: float
    comentario: str