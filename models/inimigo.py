from __future__ import annotations
from .base import Entidade, Atributos


class Inimigo(Entidade):

    def __init__(self, nome: str, vida: int, ataque: int, defesa: int):
        super().__init__(
            nome, 
            Atributos(vida=vida, ataque=ataque, defesa=defesa, vida_max=vida), 
            arquetipo="Inimigo"
        )

    def __repr__(self) -> str:
        return f"<Inimigo nome={self.nome} vida={self.atrib.vida}/{self.atrib.vida_max}>"