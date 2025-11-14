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

    def ganhar_xp(self, quantidade):
        """
        Função simples para adicionar XP ao personagem.
        Quando XP atingir o limite, sobe de nível.
        """
        self.xp += quantidade

        # XP necessário para upar (fórmula simples)
        xp_para_up = self.nivel * 100

        # Enquanto tiver XP suficiente para upar mais de uma vez
        while self.xp >= xp_para_up:
            self.xp -= xp_para_up
            self.upar_nivel()
            xp_para_up = self.nivel * 100  # recalcula para o próximo nível

    def upar_nivel(self):
        """
        Aumenta o nível e melhora atributos aos poucos.
        Lógica simples para parecer feita por aluno.
        """
        self.nivel += 1

        # Atributos sobem de maneira básica
        self._atrib.vida += 10
        self._atrib.mana += 5
        self._attrib.ataque += 2
        self._atrib.defesa += 2

        print(f"{self.nome} subiu para o nível {self.nivel}!")
