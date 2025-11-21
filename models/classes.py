from __future__ import annotations
import random
from .base import Entidade, Atributos
from .personagem import Personagem
from .item import Raridade # Importação correta

class Guerreiro(Personagem):
    """
    Subclasse de Personagem focada em força e resistência.
    Habilidade: Ataque Feroz (Alto Dano Físico).
    """
    
    CUSTO_HABILIDADE = 10
    DANO_MAXIMO = 30 
    
    def __init__(self, nome: str):
        # ATRIBUTOS BASE: A ordem deve seguir a definição em Atributos:
        # (ataque, defesa, vida_max, mana_max, _eq..., vida, mana)
        atributos = Atributos(
            ataque=15, defesa=8, vida_max=120, mana_max=30, 
            vida=120, mana=30,  
        )
        super().__init__(nome, atributos, arquetipo="Guerreiro") 

    def habilidade_especial(self) -> tuple[int, int]:
        """Executa um Ataque Feroz, consumindo Mana."""
        if self.consumir_mana(self.CUSTO_HABILIDADE):
            # O dano escala com o ataque total atual
            dano_causado = random.randint(self._atrib.ataque_total, self.DANO_MAXIMO + self._atrib.ataque_total)
            print(f"🗡️ {self.nome} desfere um **Ataque Feroz** e causa {dano_causado} de dano!")
            return dano_causado, self.CUSTO_HABILIDADE
        else:
            print(f"❌ {self.nome} não tem Mana suficiente ({self._atrib.mana}/{self._atrib.mana_max_total}).")
            return 0, 0 


class Mago(Personagem):
    """
    Subclasse de Personagem focada em magia.
    Habilidade: Bola de Fogo (Alto Dano Mágico).
    """
    
    CUSTO_HABILIDADE = 15
    DANO_MAXIMO = 45 
    
    def __init__(self, nome: str):
        atributos = Atributos(
            ataque=10, defesa=5, vida_max=80, mana_max=50, 
            vida=80, mana=50, 
        )
        super().__init__(nome, atributos, arquetipo="Mago") 

    def habilidade_especial(self) -> tuple[int, int]:
        """Conjura uma Bola de Fogo, consumindo Mana."""
        if self.consumir_mana(self.CUSTO_HABILIDADE):
            dano_causado = random.randint(self._atrib.ataque_total, self.DANO_MAXIMO + self._atrib.ataque_total)
            print(f"🔥 {self.nome} conjura uma **Bola de Fogo** e causa {dano_causado} de dano!")
            return dano_causado, self.CUSTO_HABILIDADE
        else:
            print(f"❌ {self.nome} não tem Mana suficiente ({self._atrib.mana}/{self._atrib.mana_max_total}).")
            return 0, 0

class Arqueiro(Personagem):
    """
    Subclasse de Personagem focada em agilidade e precisão.
    Habilidade: Flecha Perfurante (Dano Mínimo Elevado).
    """
    
    CUSTO_HABILIDADE = 8
    DANO_MAXIMO = 25 
    
    def __init__(self, nome: str):
        atributos = Atributos(
            ataque=18, defesa=6, vida_max=90, mana_max=25, 
            vida=90, mana=25, 
        )
        super().__init__(nome, atributos, arquetipo="Arqueiro") 

    def habilidade_especial(self) -> tuple[int, int]:
        """Dispara uma Flecha Perfurante, garantindo um dano mínimo alto."""
        if self.consumir_mana(self.CUSTO_HABILIDADE):
            # Dano Mínimo é o Ataque Total + 5, garantindo um bom hit
            dano_causado = random.randint(self._atrib.ataque_total + 5, self.DANO_MAXIMO + self._atrib.ataque_total)
            print(f"🏹 {self.nome} dispara uma **Flecha Perfurante** e causa {dano_causado} de dano!")
            return dano_causado, self.CUSTO_HABILIDADE
        else:
            print(f"❌ {self.nome} não tem Mana suficiente ({self._atrib.mana}/{self._atrib.mana_max_total}).")
            return 0, 0


class Curandeiro(Personagem):
    """
    Subclasse de Personagem focada em suporte e cura.
    Habilidade: Cura Elevada (Restaura grande quantidade de HP do usuário).
    """
    
    CUSTO_HABILIDADE = 20
    VALOR_CURA_BASE = 50 # Cura base que o skill garante
    
    def __init__(self, nome: str):
        atributos = Atributos(
            ataque=5, defesa=7, vida_max=100, mana_max=60, 
            vida=100, mana=60, 
        )
        super().__init__(nome, atributos, arquetipo="Curandeiro") 

    def habilidade_especial(self) -> tuple[int, int]:
        """Cura Elevada: Restaura uma grande quantidade de HP do usuário."""
        if self.consumir_mana(self.CUSTO_HABILIDADE):
            # Cura é o valor base + um bônus de mana_max para escala
            cura_valor = self.VALOR_CURA_BASE + (self._atrib.mana_max_total // 4)
            cura_aplicada = min(cura_valor, self._atrib.vida_max_total - self.hp_atual)
            self.hp_atual += cura_aplicada
            self.hp_atual = min(self.hp_atual, self._atrib.vida_max_total) # Garante o limite

            print(f"✨ {self.nome} conjurou **Cura Elevada** e restaurou {cura_aplicada} HP!")
            return 0, self.CUSTO_HABILIDADE # Retorna 0 de dano para o loop de combate
        else:
            print(f"❌ {self.nome} não tem Mana suficiente ({self._atrib.mana}/{self._atrib.mana_max_total}).")
            return 0, 0