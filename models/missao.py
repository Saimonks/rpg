from __future__ import annotations
from dataclasses import dataclass
from .personagem import Personagem
from .inimigo import Inimigo


@dataclass
class ResultadoMissao:
    """Resultado da missão."""
    venceu: bool = False
    xp_ganho: int = 0
    detalhes: str = "Missão simulada."


class Missao:
    """Estrutura da missão com a mecânica de combate."""

    def __init__(self, titulo: str, inimigo: Inimigo):
        self.titulo = titulo
        self.inimigo = inimigo

    def executar(self, p: Personagem) -> ResultadoMissao:
        """
        Implementação do Loop de Combate Principal (T4).
        """
        print(f"\n======================================")
        print(f"=== INICIANDO MISSÃO: {self.titulo.upper()} ===")
        print(f"Seu oponente: {self.inimigo.nome}")
        print(f"======================================")

        while p.hp_atual > 0 and self.inimigo.vivo: # Checa a vida atual do Personagem
            # 1. Mostrar Status
            print("\n--- STATUS ATUAL ---")
            print(f"{p.nome} {p.barra_hp().replace('v/', f'{p.hp_atual}/').replace(str(p.atrib.vida), str(p.hp_atual))} {p.barra_mana()}")
            print(f"{self.inimigo.nome} {self.inimigo.barra_hp()}")

            # 2. Turno do Jogador: Escolha da Ação
            print("\nO que você fará?")
            print("[1] Ataque Básico")
            print("[2] Habilidade Especial")
            print("[3] Curar-se (Cura Total)")
            print("[4] Fugir (Encerra a Missão)")
            
            op = input("Sua ação: ").strip()

            dano_causado = 0

            if op == "1":
                dano_causado = p.atacar()
            
            elif op == "2":
                dano_causado, _ = p.habilidade_especial() # Retorna dano e custo (ignorado aqui)

            elif op == "3":
                cura_valor = p.curar()
                if cura_valor > 0:
                    print(f"✨ {p.nome} se curou totalmente! HP restaurado: {cura_valor}.")
                else:
                    print(f"🛡️ {p.nome} já está com a vida máxima.")
                continue

            elif op == "4":
                print("🏃 Você fugiu da batalha.")
                return ResultadoMissao(venceu=False, detalhes="Fuga da batalha.")

            else:
                print("Ação inválida. Tente novamente.")
                continue

            # 3. Processar Dano no Inimigo
            if dano_causado > 0:
                dano_efetivo = self.inimigo.receber_dano(dano_causado)
                print(f"💥 {self.inimigo.nome} sofre {dano_efetivo} de dano efetivo.")

            # Se o inimigo morreu, encerra o loop
            if not self.inimigo.vivo:
                break
                
            # 4. Turno do Inimigo (se ainda estiver vivo)
            print(f"\n... É a vez de {self.inimigo.nome} ...")
            dano_inimigo = self.inimigo.atacar()
            dano_efetivo_recebido = p.receber_dano(dano_inimigo) # Dano no Personagem
            p.hp_atual -= dano_efetivo_recebido # Reduz a vida atual do Personagem

            print(f"🔥 {self.inimigo.nome} ataca e causa {dano_efetivo_recebido} de dano em {p.nome}.")


        # 5. Lógica de Fim de Combate (T9: Recompensas)
        
        if p.hp_atual > 0:
            xp_ganho = self.inimigo.atrib.vida_max // 3
            p.ganhar_xp(xp_ganho)
            
            print(f"\n🎉 VITÓRIA! {p.nome} derrotou o {self.inimigo.nome}!")
            return ResultadoMissao(venceu=True, xp_ganho=xp_ganho, detalhes="O inimigo foi derrotado.")
        else:
            print(f"\n💀 DERROTA! {p.nome} foi derrotado por {self.inimigo.nome}.")
            # Se derrotado, a vida atual é zero
            p.hp_atual = 0
            return ResultadoMissao(venceu=False, detalhes="O personagem foi nocauteado.")