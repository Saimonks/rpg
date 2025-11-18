from __future__ import annotations
from dataclasses import dataclass, asdict # <--- Importar 'asdict'
import random


@dataclass
class Atributos:
    """Estrutura simples de atributos."""
    vida: int
    ataque: int
    defesa: int
    chance_crit: float
    multi_crit: float 
    mana: int = 0
    vida_max: int | None = None
    mana_max: int | None = None 


class Entidade:
    """Base para Personagem e Inimigo (com lógica base de combate)."""
    
    def __init__(self, nome: str, atrib: Atributos, arquetipo: str = "NPC"):
        self._nome = nome
        self._arquetipo = arquetipo
        
        # Lógica de vida máxima
        if atrib.vida_max is None:
            atrib.vida_max = atrib.vida
        
        # Lógica de mana máxima
        if atrib.mana_max is None:
            atrib.mana_max = atrib.mana
            
        self._atrib = atrib

    # --- MÉTODO CRUCIAL PARA SALVAR ---
    def to_dict(self) -> dict:
        """ 
        Converte a Entidade e seus Atributos aninhados em um dicionário 
        seguro para JSON.
        """
        data = self.__dict__.copy()
        
        # Converte o objeto Atributos (que não é serializável) em um dicionário
        if '_atrib' in data:
            data['_atrib'] = asdict(data['_atrib'])
            
        return data
        
    @property
    def nome(self) -> str:
        """Retorna o nome da Entidade."""
        return self._nome
    
    @property
    def atrib(self) -> Atributos:
        """Retorna os atributos da Entidade."""
        return self._atrib

    @property
    def vivo(self) -> bool:
        """Verifica se a Entidade está viva (usando a vida atual do Atributos)."""
        return self._atrib.vida > 0

    def atacar(self) -> int:
        # Base + dado 1d6
        dano = self._atrib.ataque + random.randint(1, 6)

        # --- Arma ---
        if hasattr(self, "arma") and self.arma:
            dano += self.arma.dano

        # --- Crítico ---
        chance_crit = self._atrib.chance_crit
        multi_crit = self._atrib.multi_crit

        if hasattr(self, "arma") and self.arma:
            chance_crit += self.arma.chance_crit
            multi_crit = max(multi_crit, self.arma.multi_crit)

        # Aplicar crítico
        if random.random() < chance_crit:
            dano = int(dano * multi_crit)
            print(f"💥 CRÍTICO de {self.nome}! ({dano} de dano)")
        else:
            print(f"⚔️ {self.nome} atacou e causou {dano} de dano.")

        return dano

    def receber_dano(self, dano: int) -> int:
        """Processa o dano recebido, subtraindo a defesa."""
        efetivo = max(0, dano - self._atrib.defesa)
        self._atrib.vida = max(0, self._atrib.vida - efetivo)
        return efetivo
    
    def consumir_mana(self, custo: int) -> bool:
        """Tenta consumir a mana e retorna True se conseguir."""
        if self._atrib.mana >= custo:
            self._atrib.mana -= custo
            return True
        return False

    def barra_hp(self, largura: int = 20) -> str:
        """Barra de HP visual."""
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