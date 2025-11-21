from __future__ import annotations
from dataclasses import dataclass, field, asdict
import random
from typing import Any, Dict


@dataclass
class Atributos:
    """
    Estrutura de atributos da Entidade. Contém atributos base, bônus de equipamento e atributos atuais.
    A ordem dos campos é crucial para a inicialização do Dataclass.
    """
    # ATRIBUTOS BASE (Estáticos, usados na progressão de nível)
    ataque: int = 1
    defesa: int = 1
    vida_max: int = 20
    mana_max: int = 0
    
    # Bônus de Equipamento (Ajustados dinamicamente)
    _ataque_eq: int = field(default=0)
    _defesa_eq: int = field(default=0)
    _vida_max_eq: int = field(default=0)
    _mana_max_eq: int = field(default=0)
    
    # ATRIBUTOS ATUAIS (Variáveis de Estado)
    vida: int = 1 
    mana: int = 0 

    # --- Propriedades de Leitura (Total = Base + Equipamento) ---
    @property
    def ataque_total(self) -> int:
        """Calcula o ataque total (base + bônus de equipamento)."""
        return self.ataque + self._ataque_eq

    @property
    def defesa_total(self) -> int:
        """Calcula a defesa total (base + bônus de equipamento)."""
        return self.defesa + self._defesa_eq

    @property
    def vida_max_total(self) -> int:
        """Calcula a vida máxima total (base + bônus de equipamento)."""
        return self.vida_max + self._vida_max_eq

    @property
    def mana_max_total(self) -> int:
        """Calcula a mana máxima total (base + bônus de equipamento)."""
        return self.mana_max + self._mana_max_eq

    # --- MÉTODOS PARA SERIALIZAÇÃO ---
    def to_dict(self) -> Dict[str, Any]:
        """Retorna um dicionário com todos os atributos, incluindo os de equipamento."""
        return asdict(self)


class Entidade:
    """Base para Personagem e Inimigo."""
    
    def __init__(self, nome: str, atrib: Atributos, arquetipo: str = "NPC"):
        self._nome = nome
        self._arquetipo = arquetipo
        self._atrib = atrib

    def to_dict(self) -> dict:
        """Serializa a Entidade e seus Atributos para JSON."""
        data = self.__dict__.copy()
        if '_atrib' in data:
            data['_atrib'] = self._atrib.to_dict()
        return data
        
    @property
    def nome(self) -> str:
        """Retorna o nome da Entidade."""
        return self._nome
    
    @property
    def arquetipo(self) -> str: 
        """Retorna o arquétipo/tipo da Entidade."""
        return self._arquetipo
    
    @property
    def atrib(self) -> Atributos:
        """Retorna os atributos da Entidade."""
        return self._atrib

    @property
    def vivo(self) -> bool:
        """Verifica se a Entidade está viva."""
        return self._atrib.vida > 0 

    def atacar(self) -> int:
        """Ataque base fixo para Inimigos (usa ataque total)."""
        return self._atrib.ataque_total

    def receber_dano(self, dano: int) -> int:
        """Processa o dano recebido, subtraindo a defesa total."""
        efetivo = max(0, dano - self._atrib.defesa_total) 
        self._atrib.vida = max(0, self._atrib.vida - efetivo)
        return efetivo
    
    def consumir_mana(self, custo: int) -> bool:
        """Tenta consumir a mana."""
        if self._atrib.mana >= custo:
            self._atrib.mana -= custo
            return True
        return False

    def barra_hp(self, largura: int = 20) -> str:
        """Barra de HP visual (usada para Inimigos)."""
        v = max(0, self._atrib.vida)
        vmax = max(1, self._atrib.vida_max_total) 
        cheio = int(largura * v / vmax)
        return "[" + "❤️" * cheio + "-" * (largura - cheio) + f"] {v}/{vmax} HP"

    def barra_mana(self, largura: int = 20) -> str:
        """Barra de Mana visual."""
        v = max(0, self._atrib.mana)
        vmax = max(1, self._atrib.mana_max_total)
        cheio = int(largura * v / vmax)
        return "[" + "💧" * cheio + "-" * (largura - cheio) + f"] {v}/{vmax} MP"