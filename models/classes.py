from __future__ import annotations
import random
from .base import Entidade, Atributos
from .personagem import Personagem

# --- Classes Jogáveis (Subclasses) ---
# Implementam a lógica específica de habilidades, custo e dano máximo.

class Guerreiro(Personagem):
    """
    Subclasse de Personagem focada em força e resistência.
    Habilidade: Ataque Feroz (Alto Dano Físico).
    """
    # Constantes específicas da classe (Custo e Dano Máximo)
    CUSTO_HABILIDADE = 10
    DANO_MAXIMO = 30 
    
    def __init__(self, nome: str):
        # Configuração de atributos base (HP Alto, Mana Baixa)
        atributos = Atributos(vida=120, ataque=15, defesa=8, mana=30, mana_max=30, vida_max=120)
        # Chama o construtor da classe Personagem (Herança)
        super().__init__(nome, atributos, arquetipo="Guerreiro")

    # Sobrescrita do método da classe base (Polimorfismo)
    def habilidade_especial(self, alvo: Entidade | None = None) -> tuple[int, int]:
        """Executa um Ataque Feroz, consumindo Mana."""
        
        # 1. Lógica de Custo e Mana (usa o método encapsulado da classe base)
        if self.consumir_mana(self.CUSTO_HABILIDADE):
            # 2. Lógica de Dano Máximo
            # Dano entre o base e o máximo definido para a habilidade
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
    # Constantes específicas da classe (Custo e Dano Máximo)
    CUSTO_HABILIDADE = 15
    DANO_MAXIMO = 45 # Dano Máximo maior que o Guerreiro, mas custo mais alto
    
    def __init__(self, nome: str):
        # Configuração de atributos base (HP Baixo, Mana Alta)
        atributos = Atributos(vida=80, ataque=10, defesa=5, mana=50, mana_max=50, vida_max=80)
        # Chama o construtor da classe Personagem (Herança)
        super().__init__(nome, atributos, arquetipo="Mago")

    # Sobrescrita do método da classe base (Polimorfismo)
    def habilidade_especial(self, alvo: Entidade | None = None) -> tuple[int, int]:
        """Conjura uma Bola de Fogo, consumindo Mana."""
        
        # 1. Lógica de Custo e Mana (usa o método encapsulado da classe base)
        if self.consumir_mana(self.CUSTO_HABILIDADE):
            # 2. Lógica de Dano Máximo
            # Dano entre o base e o máximo definido para a habilidade
            dano_causado = random.randint(self._atrib.ataque, self.DANO_MAXIMO)
            
            print(f"🔥 {self.nome} conjura uma **Bola de Fogo**!")
            return dano_causado, self.CUSTO_HABILIDADE
        else:
            print(f"❌ {self.nome} não tem Mana suficiente ({self._atrib.mana}/{self.CUSTO_HABILIDADE}).")
            return 0, 0
