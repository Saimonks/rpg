from __future__ import annotations
import random
from .base import Entidade, Atributos
from .personagem import Personagem


class Guerreiro(Personagem):
    """
    Subclasse de Personagem focada em força e resistência.
    Habilidade: Ataque Feroz (Alto Dano Físico).
    """
    
    CUSTO_HABILIDADE = 10
    DANO_MAXIMO = 30 
    
    def __init__(self, nome: str):
    
        atributos = Atributos(vida=120, ataque=15, defesa=8, mana=30, mana_max=30, vida_max=120)
        super().__init__(nome, atributos, arquetipo="Guerreiro")

   
    def habilidade_especial(self, alvo: Entidade | None = None) -> tuple[int, int]:
        """Executa um Ataque Feroz, consumindo Mana."""
        
       
        if self.consumir_mana(self.CUSTO_HABILIDADE):
            dano_causado = random.randint(self._atrib.ataque, self.DANO_MAXIMO)
            
            print(f"🗡️ {self.nome} desfere um **Ataque Feroz**!")
            return dano_causado, self.CUSTO_HABILIDADE
        else:
            print(f"❌ {self.nome} não tem Mana suficiente ({self._atrib.mana}/{self.CUSTO_HABILIDADE}).")
            return 0, 0

class Mago(Personagem):
    """
    Subclasse de Personagem focada em magia.
    Habilidade: Bola de Fogo (Alto Dano Mágico).
    """
    
    CUSTO_HABILIDADE = 15
    DANO_MAXIMO = 45 
    
    def __init__(self, nome: str):
        
        atributos = Atributos(vida=80, ataque=10, defesa=5, mana=50, mana_max=50, vida_max=80)
        super().__init__(nome, atributos, arquetipo="Mago")

    
    def habilidade_especial(self, alvo: Entidade | None = None) -> tuple[int, int]:
        """Conjura uma Bola de Fogo, consumindo Mana."""
        
       
        if self.consumir_mana(self.CUSTO_HABILIDADE):
            dano_causado = random.randint(self._atrib.ataque, self.DANO_MAXIMO)
            
            print(f"🔥 {self.nome} conjura uma **Bola de Fogo**!")
            return dano_causado, self.CUSTO_HABILIDADE
        else:
            print(f"❌ {self.nome} não tem Mana suficiente ({self._atrib.mana}/{self.CUSTO_HABILIDADE}).")
            return 0, 0
