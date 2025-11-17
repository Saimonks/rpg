from __future__ import annotations
from dataclasses import dataclass
<<<<<<< HEAD
import random
from models.equipamentos import Arma

=======
>>>>>>> main

@dataclass
class Atributos:
    """Estrutura simples de atributos."""
    vida: int
    ataque: int
    defesa: int
    vida: int
    mana: int = 0
<<<<<<< HEAD
    chance_crit: float = 0.05
    multi_crit: float = 2.0
    vida_max: int | None = None



class Entidade:
    """Base para Personagem e Inimigo (sem regras avançadas)."""

    def __init__(self, nome: str, atrib: Atributos, arma: Arma | None = None):
=======
    vida_max: int | None = None
    mana_max: int | None = None 

class Entidade:
    """Base para Personagem e Inimigo (sem regras avançadas)."""
    def __init__(self, nome: str, atrib: Atributos):
>>>>>>> main
        self._nome = nome
        
        if atrib.vida_max is None:
            atrib.vida_max = atrib.vida
        
        if atrib.mana_max is None:
            atrib.mana_max = atrib.mana 
            
        self._atrib = atrib

    @property
    def nome(self) -> str:
        """Retorna o nome da Entidade."""
        return self._nome
    @property
    def arma(self) -> Arma | None:
        return self._arma

    @arma.setter
    def arma(self, nova_arma: Arma):
        self._arma = nova_arma
    @property
    def vivo(self) -> bool:
        """Verifica se a Entidade está viva."""
        return self._atrib.vida > 0

    def atacar(self) -> int:
        """Ataque base fixo (placeholder)."""
        return self._atrib.ataque

    def receber_dano(self, dano: int) -> int:
        """Dano efetivo simples (placeholder)."""
        efetivo = max(0, dano - self._atrib.defesa)
        self._atrib.vida = max(0, self._atrib.vida - efetivo)
        return efetivo
    
<<<<<<< HEAD
    def atacar_alvo(self, alvo: "Entidade") -> int:
        dano = self.atacar()                # calcula o dano (com crítico, arma, etc)
        efetivo = alvo.receber_dano(dano)   # aplica o dano no alvo
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
=======
    def consumir_mana(self, custo: int) -> bool:
        """Tenta consumir a mana e retorna True se conseguir."""
        if self._atrib.mana >= custo:
            self._atrib.mana -= custo
            return True
        return False

    def barra_hp(self, largura: int = 20) -> str:
        """Barra de HP meramente visual (placeholder)."""
        v = max(0, self._atrib.vida)
        vmax = max(1, self._atrib.vida_max or v)
        cheio = int(largura * v / vmax)
    
        return "[" + "❤️" * cheio + "-" * (largura - cheio) + f"] {v}/{vmax} HP"

    def barra_mana(self, largura: int = 20) -> str:
        """Barra de Mana visual."""
        v = max(0, self._atrib.mana)
        vmax = max(1, self._atrib.mana_max or v)
        cheio = int(largura * v / vmax)
        return "[" + "💧" * cheio + "-" * (largura - cheio) + f"] {v}/{vmax} MP"
>>>>>>> main
