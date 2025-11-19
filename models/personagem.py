from __future__ import annotations
import random
from .base import Entidade, Atributos
from .inventario import Inventario
from .equipamentos import Arma, Armadura

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
        self.inventario = Inventario()
        self.armadura = None
        self.arma = None

    def equipar(self, item):

        # Equipar arma
        if isinstance(item, Arma):
            if self.arma:
                # mover arma atual para inventário
                self.inventario.adicionar(self.arma)

            self.arma = item
            print(f"⚔️ {self.nome} equipou a arma: {item.nome}")
            return True

        # Equipar armadura
        if isinstance(item, Armadura):
            if self.armadura:
                self.inventario.adicionar(self.armadura)

            self.armadura = item
            print(f"🛡️ {self.nome} equipou a armadura: {item.nome}")
            return True

        print("❌ Não é possível equipar esse tipo de item.")
        return False
    
    def desequipar(self, tipo: str):
        if tipo == "arma":
            if not self.arma:
                print("Você não tem arma equipada.")
                return False
            
            self.inventario.adicionar(self.arma)
            print(f"🔻 Arma '{self.arma.nome}' foi movida para o inventário.")
            self.arma = None
            return True

        if tipo == "armadura":
            if not self.armadura:
                print("Você não tem armadura equipada.")
                return False
            
            self.inventario.adicionar(self.armadura)
            print(f"🔻 Armadura '{self.armadura.nome}' foi movida para o inventário.")
            self.armadura = None
            return True

        print("Tipo inválido para desequipar.")
        return False

    # --- IMPLEMENTAÇÃO T1: Dano Básico  ==  RETIRADO, AGR SE ENCONTRA NO BASE.PY---
    
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