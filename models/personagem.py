from __future__ import annotations
from models.base import Entidade, Atributos
from models.equipamentos import Arma
from models.classe import classes

class Personagem(Entidade):

    def __init__(self, nome: str, classe_nome: str, arma: Arma):
        dados = classes[classe_nome]

        atributos = Atributos(
            ataque=dados["ataque_base"],
            defesa=dados["defesa_base"],
            mana=dados["mana_base"],
            chance_crit=dados["chance_crit"],
            multi_crit=dados["multi_crit"],
            vida=dados["vida_base"],
        )

        super().__init__(nome, atributos, arma)
        self.classe = classe_nome
        self.descricao = dados["descricao"]
        self.nivel = 1
        self.xp = 0





    def habilidade_especial(self) -> int:
        """
        Deve retornar dano especial (ou 0 se indisponível).
        (ex.: consumir self._atrib.mana e aplicar bônus de dano)
        """
        raise NotImplementedError("Implementar habilidade especial do Personagem.")
