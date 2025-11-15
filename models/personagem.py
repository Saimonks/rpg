from __future__ import annotations
from .base import Entidade, Atributos


class Personagem(Entidade):
    """
    Classe base única do jogador.
    Esta versão NÃO implementa a lógica principal de combate.
    """

    def __init__(self, nome: str, atrib: Atributos):
        super().__init__(nome, atrib)
        self.nivel = 1
        self.xp = 0

    def calcular_dano_base(self) -> int:
        """
        Deve retornar um inteiro com o dano base do personagem.
        (ex.: usar self._atrib.ataque, aplicar aleatoriedade/crítico/etc.)
        """
        raise NotImplementedError("Implementar cálculo de dano base do Personagem.")

    def habilidade_especial(self) -> int:
        """
        Deve retornar dano especial (ou 0 se indisponível).
        (ex.: consumir self._atrib.mana e aplicar bônus de dano)
        """
        raise NotImplementedError("Implementar habilidade especial do Personagem.")

    def curar(self) -> int:
        """
        Restaura a vida do personagem até o valor máximo.
        Retorna quanto foi curado.
        """
        vida_atual = self._atrib.vida
        vida_max = self._atrib.vida_max

        if vida_atual >= vida_max:
            return 0  # já está com HP cheio

        cura = vida_max - vida_atual
        self._atrib.vida = vida_max
        return cura
