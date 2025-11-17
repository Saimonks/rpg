from __future__ import annotations
<<<<<<< HEAD
from models.base import Entidade, Atributos
from models.equipamentos import Arma
from models.classe import classes

class Personagem(Entidade):
=======
# Ajuste o import conforme a localização dos seus arquivos 'Entidade' e 'Atributos'
from .base import Entidade, Atributos 


class Personagem(Entidade):
    """
    Classe base única do jogador.
    Implementa lógica de XP/Nível e Cura, mas NÃO implementa a lógica principal de combate.
    """
>>>>>>> main

    def __init__(self, nome: str, classe_nome: str, arma: Arma):
        dados = classes[classe_nome]

        atributos = Atributos(
            ataque=dados["ataque_base"],
            defesa=dados["defesa_base"],
            mana=dados["mana_base"],
            chance_crit=dados["chance_crit"],
            multi_crit=dados["multi_crit"],
            vida=dados["vida_base"],
        )

        super().__init__(nome, atributos, arma)
        self.classe = classe_nome
        self.descricao = dados["descricao"]
        self.nivel = 1
        self.xp = 0
        
        # --- ATENÇÃO: Adicione aqui a inicialização do HP atual ---
        # A vida atual DEVE ser separada da vida máxima.
        # Assumindo que self._atrib.vida_max já está definido em Atributos/Entidade
        # Se não estiver, você precisará adicionar 'self.hp_atual = atrib.vida'
        self.hp_atual = self._atrib.vida_max 


<<<<<<< HEAD



=======
    def calcular_dano_base(self) -> int:
        """
        Deve retornar um inteiro com o dano base do personagem.
        """
        raise NotImplementedError("Implementar cálculo de dano base do Personagem.")
>>>>>>> main

    def habilidade_especial(self) -> int:
        """
        Deve retornar dano especial (ou 0 se indisponível).
        """
        raise NotImplementedError("Implementar habilidade especial do Personagem.")
    
    # --- LÓGICA DE XP E NÍVEL (patch-5) ---
    
    def ganhar_xp(self, quantidade: int):
        """
        Função para adicionar XP ao personagem e verificar se sobe de nível.
        """
        if quantidade < 0:
            return # Não processa XP negativo
            
        self.xp += quantidade
        print(f"{self.nome} ganhou {quantidade} de XP.")

        # XP necessário para upar (fórmula simples: 100 * Nível)
        xp_para_up = self.nivel * 100

        # Loop para garantir que o personagem sobe múltiplos níveis se ganhar muito XP
        while self.xp >= xp_para_up:
            self.xp -= xp_para_up
            self.upar_nivel()
            xp_para_up = self.nivel * 100  # Recalcula para o próximo nível

    def upar_nivel(self):
        """
        Aumenta o nível e melhora atributos.
        """
        self.nivel += 1

        # Aumenta os atributos base (MAX)
        # Assumindo que você mudou 'vida' para 'vida_max' na classe Atributos
        self._atrib.vida_max += 10
        self._atrib.mana += 5
        self._atrib.ataque += 2  # <--- CORRIGIDO: de '_attrib' para '_atrib'
        self._atrib.defesa += 2

        # Cura o personagem COMPLETAMENTE ao subir de nível
        self.hp_atual = self._atrib.vida_max 

        print(f"\n🎉 {self.nome} subiu para o nível {self.nivel}!")
        print(f"Status Atual: HP: {self.hp_atual}/{self._atrib.vida_max} | ATK: {self._atrib.ataque}")

    # --- LÓGICA DE CURA (método de cura) ---
    
    def curar(self) -> int:
        """
        Restaura a vida do personagem até o valor máximo.
        Retorna quanto foi curado.
        """
        vida_max = self._atrib.vida_max
        
        if self.hp_atual >= vida_max:
            return 0  # Já está com HP cheio

        cura = vida_max - self.hp_atual
        self.hp_atual = vida_max # Seta o HP atual para o máximo
        return cura