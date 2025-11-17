from __future__ import annotations
import random
from .base import Entidade, Atributos


class Personagem(Entidade):
    """
    Classe base única do jogador.
    Implementa lógica de XP/Nível e Cura.
    """

    # CORREÇÃO CRÍTICA: Adicionando 'arquetipo' no __init__.
    def __init__(self, nome: str, atrib: Atributos, arquetipo: str = "Personalizado"): 
        # Passa todos os argumentos para a classe Entidade
        super().__init__(nome, atrib, arquetipo) 
        self.nivel = 1
        self.xp = 0
        
        # HP atual é rastreado separadamente do HP máximo
        self.hp_atual = self._atrib.vida_max 

    # --- IMPLEMENTAÇÃO T1: Dano Básico ---
    def calcular_dano_base(self) -> int:
        """
        Dano do Personagem: Ataque Base + 1d6 (aleatório).
        """
        dado_aleatorio = random.randint(1, 6) 
        dano_total = self._atrib.ataque + dado_aleatorio 
        
        print(f"⚔️ {self.nome} ataca, causando **{dano_total}** de dano!")
        return dano_total
    
    def habilidade_especial(self) -> tuple[int, int]:
        """
        Será sobrescrita pelas subclasses (Guerreiro/Mago).
        Esta versão genérica não faz nada.
        """
        return 0, 0

    # --- IMPLEMENTAÇÃO T6: LÓGICA DE XP E NÍVEL ---
    def ganhar_xp(self, quantidade: int):
        """Função para adicionar XP ao personagem e verificar se sobe de nível."""
        if quantidade <= 0: return 
            
        self.xp += quantidade
        print(f"{self.nome} ganhou {quantidade} de XP.")

        xp_para_up = self.nivel * 100

        while self.xp >= xp_para_up:
            self.xp -= xp_para_up
            self.upar_nivel()
            xp_para_up = self.nivel * 100 

    def upar_nivel(self):
        """Aumenta o nível e melhora atributos."""
        self.nivel += 1

        # Aumenta atributos (Max e Atual)
        self._atrib.vida_max += 10
        self._atrib.mana_max += 5
        self._atrib.ataque += 2 
        self._atrib.defesa += 2

        # Cura completa e restaura mana ao subir de nível
        self.hp_atual = self._atrib.vida_max 
        self._atrib.mana = self._atrib.mana_max 

        print(f"\n🎉 {self.nome} subiu para o nível {self.nivel}!")
        print(f"Status Atual: HP: {self.hp_atual}/{self._atrib.vida_max} | ATK: {self._atrib.ataque}")

    def curar(self) -> int:
        """Restaura a vida do personagem até o valor máximo."""
        vida_max = self._atrib.vida_max
        
        if self.hp_atual >= vida_max:
            return 0 

        cura = vida_max - self.hp_atual
        self.hp_atual = vida_max
        return cura