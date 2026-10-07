from dataclasses import dataclass, field
from datetime import date
from enum import Enum


class PapelUsuario(str, Enum):
    ORGANIZADOR = "ORGANIZADOR"
    PARTICIPANTE = "PARTICIPANTE"
    JURADO = "JURADO"
    MENTOR = "MENTOR"

    @property
    def rotulo(self) -> str:
        rotulos = {
            "ORGANIZADOR": "Organizador",
            "PARTICIPANTE": "Participante",
            "JURADO": "Jurado",
            "MENTOR": "Mentor",
        }
        return rotulos[self.value]


@dataclass
class Usuario:
    id: int | None
    nome: str
    email: str
    senha_hash: str
    papel: PapelUsuario


@dataclass
class Hackathon:
    id: int | None
    nome: str
    data_inicio: date
    data_fim: date
    max_equipes: int
    organizador: Usuario


@dataclass
class Equipe:
    id: int | None
    nome: str
    hackathon: Hackathon
    lider: Usuario
    participantes: list[Usuario] = field(default_factory=list)

    def adicionar_participante(self, participante: Usuario):
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
class Mentoria:
    id: int | None
    mentor: Usuario
    equipe: Equipe
    comentario: str


@dataclass
class Avaliacao:
    id: int | None
    jurado: Usuario
    projeto: Projeto
    nota: float
    comentario: str
