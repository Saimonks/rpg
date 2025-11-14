from __future__ import annotations
from dataclasses import dataclass
import random


@dataclass
class Atributos:
    """Estrutura simples de atributos."""
    ataque: int
    defesa: int
    mana: int = 0
    chance_crit: float = 0.05
    multi_crit: float = 2.0
    vida: int
    vida_max: int | None = None


@dataclass
class armas:
    nome: str
    dano: int
    chance_crit: float = 0.0 
    multi_crit: float = 1.0





class Entidade:
    """Base para Personagem e Inimigo (sem regras avançadas)."""

    def __init__(self, nome: str, atrib: Atributos, arma: armas):
        self._nome = nome
        if atrib.vida_max is None:
            atrib.vida_max = atrib.vida
        self._atrib = atrib
        self._arma = arma

    @property
    def nome(self) -> str:
        return self._nome

    @property
    def vivo(self) -> bool:
        return self._atrib.vida > 0

    def atacar(self) -> int:

        dano = self._atrib.ataque


        if self.arma:
            dano += self.arma.dano

        chance_crit = self._atrib.chance_crit
        multi_crit = self._atrib.multi_crit

        if self.arma:
            chance_crit += self._arma.chance_crit
            multi_crit = max(multi_crit, self._arma.multi_crit)

        if random.random() < chance_crit:
            return int(dano * multi_crit)

        return dano


    def receber_dano(self, dano: int) -> int:
        
        defesa = self._atrib.defesa

        if random.random() < 0.10:
            efetivo = dano
        else:
            efetivo = max(1, dano - defesa)
        
        self._atrib.vida = max(0, self._atrib.vida - efetivo)

        return efetivo

def barra_hp(self, largura: int = 20) -> str:
    vida = max(0, self._atrib.vida)
    vida_max = max(1, self._atrib.vida_max)

    proporcao = vida / vida_max
    cheio = int(proporcao * largura)
    vazio = largura - cheio

    if proporcao > 0.6:
        cor = "\033[92m"   # cor verde
    elif proporcao > 0.3:
        cor = "\033[93m"   # cor amarelo
    else:
        cor = "\033[91m"  #cor vermelho

    reset = "\033[0m"

    barra = f"{cor}[{'#' * cheio}{'-' * vazio}]{reset} {vida}/{vida_max} HP"
    return barra