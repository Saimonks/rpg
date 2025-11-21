from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import Dict, List, Any, Optional


# --- ENUM DE RARIDADE ---
class Raridade(Enum):
    COMUM = "Comum"
    INCOMUM = "Incomum"
    RARO = "Raro"
    LENDARIO = "Lendário"

# --- ESTRUTURA DE ATRIBUTOS PARA ITENS DE EQUIPAMENTO ---
@dataclass
class ItemStats:
    ataque: int = 0
    defesa: int = 0
    vida_max: int = 0
    mana_max: int = 0
    def to_dict(self): return asdict(self)


# --- CLASSE BASE DO ITEM ---
@dataclass
class Item:
    nome: str
    tipo: str  # Ex: "Consumível", "Equipamento", "Tesouro"
    raridade: Raridade
    stats: ItemStats = field(default_factory=ItemStats)
    descricao: str = ""
    valor: int = 0 # Valor base do item (para compra ou venda)
    def to_dict(self): return asdict(self)


# --- BANCO DE DADOS DE ITENS (LOOT TABLE) ---
ITENS_DROP = {
    Raridade.COMUM: [
        Item("Poção de Vida Pequena", "Consumível", Raridade.COMUM, valor=20, descricao="Restaura 30% da Vida Máxima."),
        Item("Luvas de Couro", "Equipamento", Raridade.COMUM, valor=50, stats=ItemStats(defesa=1), descricao="Aumenta levemente sua defesa."),
        Item("Bandagem Simples", "Consumível", Raridade.COMUM, valor=10, descricao="Restaura 15 HP fixo."),
        Item("Cinto de Couro", "Equipamento", Raridade.COMUM, valor=40, stats=ItemStats(vida_max=5), descricao="Aumenta ligeiramente sua vitalidade."),
        # Arma Comum
        Item("Machado Enferrujado", "Equipamento", Raridade.COMUM, valor=60, stats=ItemStats(ataque=2), descricao="Um machado básico e pesado."),
    ],
    Raridade.INCOMUM: [
        Item("Poção de Mana", "Consumível", Raridade.INCOMUM, valor=35, descricao="Restaura 15 Mana."),
        Item("Elmo de Ferro", "Equipamento", Raridade.INCOMUM, valor=150, stats=ItemStats(defesa=3, vida_max=5), descricao="Um elmo que oferece boa proteção."),
        Item("Espada Longa", "Equipamento", Raridade.INCOMUM, valor=180, stats=ItemStats(ataque=4), descricao="Aumenta significativamente seu ataque."),
        Item("Adaga Amaldiçoada", "Equipamento", Raridade.INCOMUM, valor=200, stats=ItemStats(ataque=5, vida_max=-10), descricao="Alto ataque, mas drena vitalidade."),
        Item("Botas Leves", "Equipamento", Raridade.INCOMUM, valor=100, stats=ItemStats(defesa=2, mana_max=3), descricao="Defesa e um pouco de mana."),
        # Arma Incomum
        Item("Cajado Simples", "Equipamento", Raridade.INCOMUM, valor=130, stats=ItemStats(ataque=3, mana_max=5), descricao="Arma básica para magos."),
    ],
    Raridade.RARO: [
        Item("Amuleto da Vitalidade", "Equipamento", Raridade.RARO, valor=500, stats=ItemStats(vida_max=20, mana_max=5), descricao="Concede um grande bônus de vida."),
        Item("Pergaminho de Dano", "Consumível", Raridade.RARO, valor=120, descricao="Aumenta o ataque em +10 na próxima rodada (efeito no combate)."),
        Item("Poção de Força", "Consumível", Raridade.RARO, valor=150, descricao="Aumenta o dano do ataque básico em +15 temporariamente."),
        Item("Anel de Batalha", "Equipamento", Raridade.RARO, valor=450, stats=ItemStats(ataque=3, defesa=3), descricao="Um anel que equilibra ataque e defesa."),
        # Arma Rara
        Item("Arco de Caça", "Equipamento", Raridade.RARO, valor=600, stats=ItemStats(ataque=7, vida_max=10), descricao="Permite ataques rápidos e precisos."),
    ],
    Raridade.LENDARIO: [
        Item("Coração do Dragão", "Equipamento", Raridade.LENDARIO, valor=1500, stats=ItemStats(ataque=8, defesa=5, vida_max=30, mana_max=10), descricao="Poder de um dragão ancestral."),
        Item("Manto da Floresta", "Equipamento", Raridade.LENDARIO, valor=1600, stats=ItemStats(defesa=7, mana_max=15), descricao="Bônus de defesa e mana."),
        Item("Cajado da Caverna", "Equipamento", Raridade.LENDARIO, valor=1800, stats=ItemStats(ataque=10, mana_max=5), descricao="Alto dano mágico."),
        Item("Selo das Ruínas", "Equipamento", Raridade.LENDARIO, valor=1400, stats=ItemStats(defesa=4, vida_max=35), descricao="Proteção e vitalidade extras."),
        Item("Armadura de Obsidiana", "Equipamento", Raridade.LENDARIO, valor=2000, stats=ItemStats(defesa=12, vida_max=40, ataque=-5), descricao="Defesa impenetrável, mas é muito pesada."),
        Item("Coroa do Conhecimento", "Equipamento", Raridade.LENDARIO, valor=2200, stats=ItemStats(mana_max=50, vida_max=10, defesa=2), descricao="Aumenta drasticamente o limite de mana."),
        # Arma Lendária
        Item("Lâmina Arcana", "Equipamento", Raridade.LENDARIO, valor=3000, stats=ItemStats(ataque=15, mana_max=20), descricao="Uma espada imbuída de magia pura."),
    ]
}

# --- FUNÇÃO PARA PEGAR DADOS DE UM ITEM ---
def get_item_by_name(nome: str) -> Item | None:
    """Busca um item na lista de drops pelo nome."""
    for raridade in ITENS_DROP.values():
        for item in raridade:
            if item.nome == nome:
                return item
    return None

# --- CLASSE INVENTARIO ---
@dataclass
class Inventario:
    """Um container simples que armazena itens."""
    itens: Dict[str, int] = field(default_factory=dict) 
    moedas: int = 0 # Moeda do jogo

    def adicionar_item(self, item: Item, quantidade: int = 1):
        # Apenas adiciona ao inventário
        self.itens[item.nome] = self.itens.get(item.nome, 0) + quantidade

    def remover_item(self, nome: str, quantidade: int = 1) -> bool:
        """Remove um item do inventário."""
        if self.itens.get(nome, 0) >= quantidade:
            self.itens[nome] -= quantidade
            if self.itens[nome] == 0:
                del self.itens[nome]
            return True
        return False

    def get_item(self, nome: str) -> Optional[Item]:
        """Retorna o objeto Item real se ele estiver no inventário (ignora quantidade)."""
        if nome in self.itens:
            return get_item_by_name(nome)
        return None

    def listar_itens(self):
        """Imprime o inventário formatado, mostrando os bônus dos equipamentos."""
        if not self.itens and self.moedas == 0:
            print("O inventário está vazio.")
            return

        print("\n--- INVENTÁRIO ---")
        print(f"Moedas: {self.moedas}")
        
        for nome in sorted(self.itens.keys()):
            qtd = self.itens[nome]
            item_obj = get_item_by_name(nome)
            
            if not item_obj:
                print(f"[{qtd}x] {nome} (Erro de Item Desconhecido)")
                continue

            raridade = item_obj.raridade.value
            detalhe_stats = ""
            
            if item_obj.tipo == "Equipamento":
                stats = []
                # Adaptação para valores negativos (trade-offs)
                if item_obj.stats.ataque != 0: 
                    op = '+' if item_obj.stats.ataque > 0 else ''
                    stats.append(f"ATK {op}{item_obj.stats.ataque}")
                if item_obj.stats.defesa != 0: 
                    op = '+' if item_obj.stats.defesa > 0 else ''
                    stats.append(f"DEF {op}{item_obj.stats.defesa}")
                if item_obj.stats.vida_max != 0: 
                    op = '+' if item_obj.stats.vida_max > 0 else ''
                    stats.append(f"HP {op}{item_obj.stats.vida_max}")
                if item_obj.stats.mana_max != 0: 
                    op = '+' if item_obj.stats.mana_max > 0 else ''
                    stats.append(f"MP {op}{item_obj.stats.mana_max}")
                
                if stats:
                    detalhe_stats = f" ({', '.join(stats)})"
                
            elif item_obj.tipo == "Consumível":
                 detalhe_stats = f" ({item_obj.descricao})"
            
            print(f"[{qtd}x] {nome} ({raridade}){detalhe_stats} | Valor: {item_obj.valor}")
            
    def to_dict(self) -> Dict[str, Any]:
        """Serializa o Inventario."""
        return asdict(self)