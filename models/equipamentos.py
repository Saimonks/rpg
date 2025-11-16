from dataclasses import dataclass

@dataclass
class Arma:
    nome: str
    dano: int
    chance_crit: float = 0.0 
    multi_crit: float = 1.0

ARMAS_INICIAIS = {
    "Guerreiro": Arma("Espada Curta", dano=5),
    "Mago": Arma("Cajado de Carvalho", dano=3),
    "Arqueiro": Arma("Arco Simples", dano=4),
    "Curandeiro": Arma("Cajado Leve", dano=2),
}