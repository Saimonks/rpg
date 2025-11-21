from __future__ import annotations
import random
from dataclasses import asdict, dataclass, field
from typing import List, Optional, Literal, Dict, Any

# Importações internas (CORRIGIDA: 'Inventario' está em '.item')
from .base import Entidade, Atributos 
from .item import Inventario, Item, ItemStats, Raridade, get_item_by_name 

class Personagem(Entidade):
    
    def __init__(self, nome: str, atrib: Atributos, arquetipo: str = "Personalizado"): 
        super().__init__(nome, atrib, arquetipo) 
        self.nivel = 1
        self.xp = 0
        
        self.hp_atual = self._atrib.vida_max_total 
        self.inventario = Inventario() 
        
        # SLOTS DE EQUIPAMENTO
        self.arma_equipada: Item | None = None
        self.armadura_equipada: Item | None = None

    # --- NOVO MÉTODO: BARRA DE XP ---
    def barra_xp(self, largura: int = 25) -> str:
        """Barra de XP visual, mostrando progresso para o próximo nível."""
        xp_necessario_prox_nivel = self.nivel * 100
        porcentagem = (self.xp / xp_necessario_prox_nivel) if xp_necessario_prox_nivel > 0 else 1.0
        cheio = int(largura * porcentagem)
        
        return f"[LVL {self.nivel}] [" + "⭐" * cheio + "-" * (largura - cheio) + f"] {self.xp}/{xp_necessario_prox_nivel} XP"

    # --- LÓGICA DE BÔNUS DE EQUIPAMENTO ---
    def _aplicar_bonus_equipamento(self, item: Item) -> None:
        if not item.stats: return
        self._atrib._ataque_eq += item.stats.ataque
        self._atrib._defesa_eq += item.stats.defesa
        self._atrib._vida_max_eq += item.stats.vida_max
        self._atrib._mana_max_eq += item.stats.mana_max
        
        # Ajusta HP e MP atuais para o novo máximo
        if item.stats.vida_max > 0:
            self.hp_atual += item.stats.vida_max
        self.hp_atual = min(self.hp_atual, self._atrib.vida_max_total)
        self._atrib.mana = min(self._atrib.mana, self._atrib.mana_max_total)
        print(f"✅ Bônus do item '{item.nome}' aplicado!")

    def _remover_bonus_equipamento(self, item: Item) -> None:
        if not item.stats: return
        self._atrib._ataque_eq -= item.stats.ataque
        self._atrib._defesa_eq -= item.stats.defesa
        self._atrib._vida_max_eq -= item.stats.vida_max
        self._atrib._mana_max_eq -= item.stats.mana_max
        
        # Ajusta o HP atual, garantindo que não fique acima do novo máximo
        if item.stats.vida_max > 0:
            self.hp_atual = min(self.hp_atual, self._atrib.vida_max_total)
        print(f"❌ Bônus do item '{item.nome}' removido.")

    # --- GESTÃO DE EQUIPAMENTO (CORREÇÃO DE SLOT) ---
    def equipar_item(self, nome_item: str) -> bool:
        """Equipa o item e aplica bônus."""
        item = get_item_by_name(nome_item)
        if not item or item.tipo != "Equipamento": 
            print(f"Item '{nome_item}' não encontrado ou não é equipamento.")
            return False
        if not self.inventario.remover_item(item.nome): 
            print(f"❌ Você não possui '{item.nome}' no inventário.")
            return False

        # LÓGICA DE SLOT CORRIGIDA para incluir todos os itens
        slot = ""
        # Itens de Ataque (Arma)
        if item.nome in [
            "Espada Longa", "Coração do Dragão", "Cajado da Caverna", 
            "Adaga Amaldiçoada", "Machado Enferrujado", "Cajado Simples", 
            "Arco de Caça", "Lâmina Arcana"
        ]: 
            slot = "arma"
        # Itens de Defesa/Acessório (Armadura)
        elif item.nome in [
            "Luvas de Couro", "Elmo de Ferro", "Amuleto da Vitalidade", 
            "Manto da Floresta", "Selo das Ruínas", "Botas Leves", 
            "Cinto de Couro", "Anel de Batalha", "Armadura de Obsidiana", 
            "Coroa do Conhecimento"
        ]: 
            slot = "armadura"
        else: 
            print(f"⚠️ Não foi possível determinar o slot de '{item.nome}'.")
            self.inventario.adicionar_item(item) # Devolve o item
            return False

        slot_equipar_name = f"{slot}_equipada"
        item_antigo = getattr(self, slot_equipar_name)

        if item_antigo:
            self.desequipar_item(slot)
        
        setattr(self, slot_equipar_name, item)
        self._aplicar_bonus_equipamento(item)

        print(f"✅ Item '{item.nome}' equipado no slot {slot.title()}!")
        return True

    def desequipar_item(self, slot: Literal["arma", "armadura"]) -> bool:
        """Desequipa o item e remove bônus."""
        slot_name = f"{slot}_equipada"
        item = getattr(self, slot_name)

        if not item: return False
        
        self._remover_bonus_equipamento(item)
        self.inventario.adicionar_item(item)
        setattr(self, slot_name, None)

        print(f"✅ Item '{item.nome}' desequipado e movido para o inventário.")
        return True
    
    # --- COMBATE, CURA E PROGRESSÃO (Demais métodos) ---
    def curar(self) -> int:
        """Cura total para o novo máximo."""
        vida_max = self._atrib.vida_max_total 
        if self.hp_atual >= vida_max: return 0 
        cura = vida_max - self.hp_atual
        self.hp_atual = vida_max
        return cura
    
    def processar_dano_recebido(self, dano_base: int) -> int:
        """Calcula dano efetivo e atualiza HP atual (usa defesa total)."""
        dano_efetivo = max(0, dano_base - self._atrib.defesa_total)
        self.hp_atual -= dano_efetivo
        self.hp_atual = max(0, self.hp_atual)
        return dano_efetivo

    def calcular_dano_base(self) -> int:
        """Dano do Personagem: Ataque Total + 1d6 (aleatório)."""
        dano_total = self._atrib.ataque_total + random.randint(1, 6) 
        print(f"⚔️ {self.nome} ataca, causando **{dano_total}** de dano!")
        return dano_total

    def habilidade_especial(self) -> tuple[int, int]: return 0, 0 

    def ganhar_xp(self, quantidade: int):
        if quantidade <= 0: return 
        self.xp += quantidade
        print(f"{self.nome} ganhou {quantidade} de XP.")
        xp_para_up = self.nivel * 100
        while self.xp >= xp_para_up:
            self.xp -= xp_para_up
            self.upar_nivel()
            xp_para_up = self.nivel * 100 

    def upar_nivel(self):
        self.nivel += 1
        self._atrib.vida_max += 10
        self._atrib.mana_max += 5
        self._atrib.ataque += 2 
        self._atrib.defesa += 2
        self.hp_atual = self._atrib.vida_max_total 
        self._atrib.mana = self._atrib.mana_max_total 
        print(f"\n🎉 {self.nome} subiu para o nível {self.nivel}!")
        print(f"Status Atual: HP: {self.hp_atual}/{self._atrib.vida_max_total} | ATK: {self._atrib.ataque_total}")

    def usar_consumivel(self, item_nome: str) -> bool:
        """Processa o uso de um item consumível do inventário."""
        item_obj = get_item_by_name(item_nome)
        if not item_obj or item_obj.tipo != "Consumível": return False
        if not self.inventario.remover_item(item_nome): return False
            
        if "Poção de Vida Pequena" == item_nome:
            cura_valor = int(self._atrib.vida_max_total * 0.3) 
            self.hp_atual = min(self._atrib.vida_max_total, self.hp_atual + cura_valor)
            print(f"💉 {self.nome} usou {item_nome} e curou {cura_valor} HP!")
        elif "Poção de Mana" == item_nome:
            mana_restaurada = 15
            self._atrib.mana = min(self._atrib.mana_max_total, self._atrib.mana + mana_restaurada)
            print(f"💧 {self.nome} usou {item_nome} e restaurou {mana_restaurada} MP!")
        
        return True

    def to_dict(self) -> Dict[str, Any]:
        """Serializa o Personagem para Save/Load."""
        return {
            "_nome": self._nome,
            "_arquetipo": self._arquetipo,
            "_atrib": self._atrib.to_dict(),
            "nivel": self.nivel,
            "xp": self.xp,
            "hp_atual": self.hp_atual,
            "inventario": self.inventario.to_dict(),
            "arma_equipada": asdict(self.arma_equipada) if self.arma_equipada else None,
            "armadura_equipada": asdict(self.armadura_equipada) if self.armadura_equipada else None,
        }