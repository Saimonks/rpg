from __future__ import annotations
from .base import Entidade, Atributos


class Inimigo(Entidade):
    """
    Inimigo genérico. Pode ser um Inimigo comum ou um Chefe.
    """

    def __init__(self, nome: str, vida: int, ataque: int, defesa: int):
        # A vida máxima é definida como a vida inicial.
        # Os inimigos não usam mana_max nem mana, por isso são definidos como 0.
        super().__init__(
            nome, 
            Atributos(vida=vida, ataque=ataque, defesa=defesa, vida_max=vida, mana=0, mana_max=0), 
            arquetipo="Inimigo"
        )
        # Observação: item_drop_garantido e xp_recompensa serão adicionados via setattr em jogo.py 
        # se esta instância for um Chefe (Boss).

    def __repr__(self) -> str:
        """Representação do objeto Inimigo para depuração."""
        return f"<Inimigo nome={self.nome} vida={self.atrib.vida}/{self.atrib.vida_max_total}>"