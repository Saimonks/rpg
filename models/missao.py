from __future__ import annotations
from dataclasses import dataclass
import random 
from .personagem import Personagem
from .inimigo import Inimigo
from .item import Item, ITENS_DROP, Raridade, get_item_by_name 


@dataclass
class ResultadoMissao:
    """Resultado da missão."""
    venceu: bool = False
    xp_ganho: int = 0
    detalhes: str = "Missão simulada."

class Missao:
    
    def __init__(self, titulo: str, inimigo: Inimigo):
        self.titulo = titulo
        self.inimigo = inimigo

    # --- LÓGICA DE DROP DE ITEM ---
    def _gerar_recompensa(self, dificuldade: str) -> Item | None:
        """
        Gera um item aleatório com base nas chances de drop.
        A chance de drop depende da dificuldade da missão (ou se é um Boss).
        """
        # Se for um Boss, o item de drop está garantido e é tratado na Missao.executar
        if dificuldade == "Boss":
            item_nome = getattr(self.inimigo, 'item_drop_garantido', None)
            if item_nome:
                return get_item_by_name(item_nome)
            return None
            
        # Definindo as chances de drop (em percentual) baseado na dificuldade
        chances_base = {
            Raridade.COMUM: 70,
            Raridade.INCOMUM: 25,
            Raridade.RARO: 5,
            Raridade.LENDARIO: 0, 
        }
        
        # Ajusta as chances de raridade para dificuldades maiores
        if dificuldade == "Média":
            chances_base[Raridade.COMUM] = 50
            chances_base[Raridade.INCOMUM] = 35
            chances_base[Raridade.RARO] = 10
            chances_base[Raridade.LENDARIO] = 5
        elif dificuldade == "Difícil":
            chances_base[Raridade.COMUM] = 30
            chances_base[Raridade.INCOMUM] = 40
            chances_base[Raridade.RARO] = 20
            chances_base[Raridade.LENDARIO] = 10
        
        # Sorteia a raridade (roll de 1 a 100)
        roll_raridade = random.randint(1, 100)
        
        raridade_sorteada = None
        soma_chance = 0
        
        # Itera sobre as chances para determinar a raridade
        for raridade, chance in chances_base.items():
            soma_chance += chance
            if roll_raridade <= soma_chance:
                raridade_sorteada = raridade
                break

        if raridade_sorteada and ITENS_DROP.get(raridade_sorteada):
            # Escolhe um item aleatório dentro da raridade sorteada
            return random.choice(ITENS_DROP[raridade_sorteada])
            
        return None


    def executar(self, p: Personagem, dificuldade: str = "Fácil") -> ResultadoMissao: 
        """ Implementação do Loop de Combate Principal. """
        
        print(f"\n======================================")
        print(f"=== INICIANDO MISSÃO: {self.titulo.upper()} ===")
        print(f"Seu oponente: {self.inimigo.nome}")
        print(f"======================================")

        while p.hp_atual > 0 and self.inimigo.vivo: 
            # 1. Mostrar Status
            print("\n--- STATUS ATUAL ---")
            
            # Usando vida_max_total para exibição correta
            hp_max_total = p._atrib.vida_max_total
            # Exibe a barra de HP do Personagem
            hp_info = f"[{'❤️' * int(20 * p.hp_atual / hp_max_total) if hp_max_total > 0 else 0} {'-' * (20 - int(20 * p.hp_atual / hp_max_total))}] {p.hp_atual}/{hp_max_total} HP"
            
            print(f"{p.nome} {hp_info} {p.barra_mana()}")
            print(f"{self.inimigo.nome} {self.inimigo.barra_hp()}")

            # 2. Turno do Jogador: Escolha da Ação
            print("\nO que você fará?")
            print("[1] Ataque Básico")
            print("[2] Habilidade Especial")
            print("[3] Usar Consumível") 
            print("[4] Fugir (Encerra a Missão)")
            
            op = input("Sua ação: ").strip()

            dano_causado = 0

            if op == "1":
                dano_causado = p.calcular_dano_base()
            
            elif op == "2":
                dano_causado, _ = p.habilidade_especial()

            elif op == "3":
                # --- LÓGICA DE CONSUMÍVEL EM BATALHA ---
                
                # Lista consumíveis disponíveis
                consumables = [name for name, count in p.inventario.itens.items() 
                               if get_item_by_name(name) and get_item_by_name(name).tipo == "Consumível"]
                
                if not consumables:
                    print("❌ Você não tem consumíveis no inventário.")
                    continue
                
                print("\n--- CONSUMÍVEIS DISPONÍVEIS ---")
                for i, name in enumerate(consumables):
                    print(f"[{i+1}] {name} ({p.inventario.itens[name]}x)")
                
                print("[0] Cancelar")
                
                try:
                    escolha = input("Selecione o NÚMERO do item para usar: ").strip()
                    if escolha == '0':
                        continue
                        
                    idx = int(escolha) - 1
                    if 0 <= idx < len(consumables):
                        item_nome = consumables[idx]
                        # Chama o método que usa, remove e aplica o efeito
                        if p.usar_consumivel(item_nome): 
                            # Se o uso foi bem-sucedido (True), pula o ataque do inimigo e volta ao loop
                            continue 
                    else:
                        print("Escolha inválida.")
                except ValueError:
                    print("Entrada inválida.")
                
                continue # Volta ao início do loop para reavaliar o turno

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

            if not self.inimigo.vivo:
                break
                
            # 4. Turno do Inimigo (se ainda estiver vivo)
            print(f"\n... É a vez de {self.inimigo.nome} ...")
            dano_inimigo_base = self.inimigo.atacar()
            
            # Usa o novo método para processar dano no Personagem (com defesa total)
            dano_efetivo_recebido = p.processar_dano_recebido(dano_inimigo_base) 
            
            print(f"🔥 {self.inimigo.nome} ataca e causa {dano_efetivo_recebido} de dano em {p.nome}.")


        # 5. Lógica de Fim de Combate (Recompensas)
        
        if p.hp_atual > 0:
            # Recompensa de XP: Se for Boss (tem xp_recompensa), usa valor fixo, senão, usa a fórmula padrão
            xp_ganho = getattr(self.inimigo, 'xp_recompensa', self.inimigo.atrib.vida_max // 3)
            
            p.ganhar_xp(xp_ganho)
            
            print(f"\n🎉 VITÓRIA! {p.nome} derrotou o {self.inimigo.nome}!")
            
            # --- LÓGICA DE DROP DE ITEM ---
            item_dropado = self._gerar_recompensa(dificuldade=dificuldade) 
            
            if item_dropado:
                print(f"💎 RECOMPENSA: Você encontrou {item_dropado.nome} ({item_dropado.raridade.value})!")
                # Exibe os stats para itens de equipamento
                if item_dropado.tipo == "Equipamento" and (item_dropado.stats.ataque != 0 or item_dropado.stats.defesa != 0 or item_dropado.stats.vida_max != 0 or item_dropado.stats.mana_max != 0):
                    stats = item_dropado.stats
                    stats_display = f"(ATK +{stats.ataque} / DEF +{stats.defesa} / HP +{stats.vida_max} / MP +{stats.mana_max})"
                    print(f"   {stats_display}")

                p.inventario.adicionar_item(item_dropado)
            else:
                 print("⭐ Você não encontrou nenhum item.")

            return ResultadoMissao(venceu=True, xp_ganho=xp_ganho, detalhes="O inimigo foi derrotado.")
        else:
            print(f"\n💀 DERROTA! {p.nome} foi derrotado por {self.inimigo.nome}.")
            p.hp_atual = 0
            return ResultadoMissao(venceu=False, detalhes="O personagem foi nocauteado.")