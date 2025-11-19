from enum import Enum
import random

class Raridade (Enum):
    COMUM = 1
    INCOMUM = 2
    RARO = 3
    EPICO = 4
    LENDARIO = 5

class Equipamento:
    def __init__(self, nome: str, raridade: Raridade):
        self.nome = nome
        self.raridade = raridade

    def __repr__(self):
        return f"{self.nome} ({self.raridade.name})"
    
class Arma (Equipamento):
    def __init__(
            self,
            nome: str,
            dano: int,
            chance_crit: float,
            multi_crit: float,
            raridade: Raridade
        ):

        super().__init__(nome, raridade)
        self.dano = dano
        self.chance_crit = chance_crit
        self.multi_crit = multi_crit

    def detalhes(self):
        return(
            f"Arma {self.nome}\n"
            f"Raridade: {self.raridade.name}\n"
            f"Dano: +{self.dano}\n"
            f"Crítico: +{self.chance_crit*100:.1f}% | x{self.multi_crit}"
        )



TABELA_ARMAS = {
    Raridade.COMUM: [
        ("Adaga Enferrujada", 2, 0.00, 1.5),
        ("Espada Velha", 3, 0.01, 1.6),
    ],
    Raridade.INCOMUM: [
        ("Espada de Ferro", 5, 0.02, 1.7),
        ("Machadinha Afiada", 6, 0.03, 1.8),
    ],
    Raridade.RARO: [
        ("Espada Longa", 8, 0.05, 2.0),
        ("Machado Duplo", 9, 0.04, 2.1),
    ],
    Raridade.EPICO: [
        ("Lâmina das Sombras", 12, 0.10, 2.2),
        ("Espada Rúnica", 14, 0.12, 2.3),
    ],
    Raridade.LENDARIO: [
        ("Espada do Rei Ancestral", 20, 0.20, 2.5),
        ("Quebradora de Mundos", 25, 0.25, 3.0),
    ]
}


def gerar_arma_por_raridade(raridade: Raridade) -> Arma:
    lista = TABELA_ARMAS[raridade]
    nome, dano, chance_crit, multi_crit = random.choice(lista)
    return Arma(nome, dano, chance_crit, multi_crit, raridade)

def gerar_drop_arma() -> Arma:
    chance = random.random()

    if chance < 0.60:
        raridade = Raridade.COMUM
    elif chance < 0.85:
        raridade = Raridade.INCOMUM
    elif chance < 0.95:
        raridade = Raridade.RARO
    elif chance < 0.99:
        raridade = Raridade.EPICO
    else:
        raridade = Raridade.LENDARIO

    return gerar_arma_por_raridade(raridade)


TABELA_ARMAS_MAGOS = {
    Raridade.COMUM: [
        ("Cajado de Madeira", 1, 0.01, 1.5),
        ("Varinha Simples", 2, 0.02, 1.5),
    ],
    Raridade.INCOMUM: [
        ("Cajado de Ferro", 3, 0.03, 1.6),
        ("Varinha Afiada", 4, 0.04, 1.7),
    ],
    Raridade.RARO: [
        ("Cajado de Fogo", 6, 0.05, 1.8),
        ("Varinha de Gelo", 7, 0.06, 1.9),
    ],
    Raridade.EPICO: [
        ("Cajado Arcano", 10, 0.10, 2.0),
        ("Varinha das Estrelas", 12, 0.12, 2.1),
    ],
    Raridade.LENDARIO: [
        ("Cajado do Grande Mago", 15, 0.20, 2.5),
        ("Varinha do Destino", 18, 0.25, 2.8),
    ]
}

def gerar_arma_mago(raridade: Raridade) -> Arma:
    lista = TABELA_ARMAS_MAGOS[raridade]
    nome, dano, chance_crit, multi_crit = random.choice(lista)
    return Arma(nome, dano, chance_crit, multi_crit, raridade)

def gerar_drop_arma_mago() -> Arma:
    chance = random.random()

    if chance < 0.60:
        raridade = Raridade.COMUM
    elif chance < 0.85:
        raridade = Raridade.INCOMUM
    elif chance < 0.95:
        raridade = Raridade.RARO
    elif chance < 0.99:
        raridade = Raridade.EPICO
    else:
        raridade = Raridade.LENDARIO

    return gerar_arma_mago(raridade)



# ARMADURAS 



class Armadura(Equipamento):
    def __init__(self, nome: str, defesa: int, raridade: Raridade):
        super().__init__(nome, raridade)
        self.defesa = defesa

    def detalhes(self):
        return (
            f"Armadura {self.nome}\n"
            f"Raridade: {self.raridade.name}\n"
            f"Defesa: +{self.defesa}"
        )

TABELA_ARMADURAS = {
    Raridade.COMUM: [
        ("Roupa de Linho", 1),
        ("Armadura de Couro Velha", 2),
    ],
    Raridade.INCOMUM: [
        ("Cota de Couro Reforçada", 4),
        ("Armadura de Ferro Leve", 5),
    ],
    Raridade.RARO: [
        ("Cota de Malha", 7),
        ("Armadura de Aço Polido", 8),
    ],
    Raridade.EPICO: [
        ("Armadura Dracônica", 12),
        ("Placas Rúnicas", 14),
    ],
    Raridade.LENDARIO: [
        ("Armadura do Rei Ancestral", 20),
        ("Couraça Celestial", 22),
    ]
}
def gerar_armadura_guerreiro(raridade: Raridade) -> Armadura:
    nome, defesa = random.choice(TABELA_ARMADURAS[raridade])
    return Armadura(nome, defesa, raridade)


def gerar_drop_armadura() -> Armadura:
    chance = random.random()

    if chance < 0.60: raridade = Raridade.COMUM
    elif chance < 0.85: raridade = Raridade.INCOMUM
    elif chance < 0.95: raridade = Raridade.RARO
    elif chance < 0.99: raridade = Raridade.EPICO
    else: raridade = Raridade.LENDARIO

    return gerar_armadura_guerreiro(raridade)

TABELA_ARMADURAS_MAGOS = {
    Raridade.COMUM: [
        ("Manto Simples",  2),
        ("Túnica de Algodão", 1, 3),
    ],
    Raridade.INCOMUM: [
        ("Manto Encantado", 4),
        ("Túnica de Seda Arcana", 5),
    ],
    Raridade.RARO: [
        ("Manto dos Elementos", 7),
        ("Túnica Estelar", 6),
    ],
    Raridade.EPICO: [
        ("Manto Arcano Superior", 10),
        ("Túnica do Vazio", 12),
    ],
    Raridade.LENDARIO: [
        ("Manto do Arquimago Supremo", 15),
        ("Túnica do Sábio Eterno", 18),
    ]
}

def gerar_armadura_mago(raridade: Raridade) -> Armadura:
    lista = TABELA_ARMADURAS_MAGOS[raridade]
    nome, defesa = random.choice(lista)
    return Armadura(nome, defesa, raridade)

def gerar_drop_armadura_mago() -> Armadura:
    chance = random.random()

    if chance < 0.60:
        raridade = Raridade.COMUM
    elif chance < 0.85:
        raridade = Raridade.INCOMUM
    elif chance < 0.95:
        raridade = Raridade.RARO
    elif chance < 0.99:
        raridade = Raridade.EPICO
    else:
        raridade = Raridade.LENDARIO

    return gerar_armadura_mago(raridade)
