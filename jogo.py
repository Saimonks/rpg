from __future__ import annotations
import random
import sys
from typing import Dict, Any, List, Literal, Optional

# Importações de Classes e Modelos (Assumimos que estão em 'models' e 'utils')
from models.personagem import Personagem 
from models.inimigo import Inimigo
from models.missao import Missao, ResultadoMissao
from models.classes import Guerreiro, Mago, Arqueiro, Curandeiro # Subclasses do Personagem
from models.base import Atributos # Dataclass para atributos
from models.item import get_item_by_name, ITENS_DROP # Usado para Chefe e Loja
from utils.repositorio import Repositorio # Lógica de Save/Load

# ----------------------------------------------------------------------
# --- CONSTANTES GLOBAIS ---
# ----------------------------------------------------------------------

# Tabela de Inimigos Comuns (por Cenário)
INIMIGOS_TABLE = {
    "Floresta Sombria": [
        ("Goblin", 30, 8, 3),    # Vida, Ataque, Defesa
        ("Lobo Enraivecido", 40, 12, 5),
    ],
    "Caverna dos Cristais": [
        ("Morcego Gigante", 50, 15, 6),
        ("Slime Brilhante", 70, 10, 8),
    ],
    "Ruínas Antigas": [
        ("Zumbi Despertado", 60, 18, 5),
        ("Esqueleto Arcano", 80, 20, 10),
    ],
}

# Tabela de Chefes (BOSS) - Mapeia Cenário -> (Nome, Vida, Ataque, Defesa, Nome do Item Dropado)
BOSS_TABLE: Dict[str, tuple[str, int, int, int, str]] = {
    "Floresta Sombria": ("Ancião Raiz", 250, 25, 10, "Manto da Floresta"),
    "Caverna dos Cristais": ("Golem de Pedra", 300, 20, 15, "Cajado da Caverna"),
    "Ruínas Antigas": ("Espectro Guardião", 200, 30, 5, "Selo das Ruínas"),
}

# Itens que a loja sempre vende (consumíveis básicos)
ITENS_LOJA_CONSUMIVEIS = ["Poção de Vida Pequena", "Poção de Mana", "Bandagem Simples"]


# ----------------------------------------------------------------------
# --- CLASSE PRINCIPAL DO JOGO ---
# ----------------------------------------------------------------------

class Jogo:
    
    def __init__(self):
        # Inicializa o personagem como None. Será carregado ou criado.
        self.personagem: Personagem | None = None
        self.missao_config = {
            "cenario": "Floresta Sombria",
            "dificuldade": "Fácil"
        }
        self.repositorio = Repositorio()
        self._save_padrao = "save_data.json" # Define o nome do save padrão

    def menu_principal(self):
        """Método principal do loop de jogo (Menu de Navegação)."""
        
        # Tenta carregar o jogo automaticamente (útil para sessões rápidas)
        self._carregar_jogo_silencioso(self._save_padrao) 
        
        while True:
            # 1. Verifica se o save existe para o menu inicial
            save_existe = self.repositorio.save_padrao_existe(self._save_padrao)
            
            if not self.personagem:
                
                # --- Menu de Início (Sem Personagem) ---
                print("\n=== PY-RPG: BEM-VINDO ===")
                
                if save_existe:
                    print("[1] Criar Novo Personagem")
                    print("[2] Carregar Jogo Salvo")
                    print("[3] Sair")
                else:
                    print("[1] Criar Novo Personagem")
                    print("[2] Sair")
                
                op = input("> ").strip()
                
                if op == '1':
                    self._criar_personagem()
                elif op == '2' and save_existe:
                    self._carregar_jogo_interativo(self._save_padrao)
                elif op == '2' and not save_existe:
                    print("Até logo!")
                    sys.exit()
                elif op == '3' and save_existe:
                    print("Até logo!")
                    sys.exit()
                else:
                    print("Opção inválida.")
                
            else:
                # --- Menu Principal (Com Personagem Carregado) ---
                print(f"\n=== RPG: {self.personagem.nome.upper()} ===")
                print(self.personagem.barra_xp(largura=30))
                print(f"❤️ HP: {self.personagem.hp_atual}/{self.personagem.atrib.vida_max_total} | 💰 {self.personagem.inventario.moedas} moedas")
                print("\n--- AÇÕES ---")
                print("[1] Aventura (Missão e Cenários)")
                print("[2] Personagem (Status e Equipamento)")
                print("[3] Loja")
                print("[4] Sistema (Salvar e Carregar)")
                print("[0] Sair")
                
                op = input("> ").strip()
                
                if op == '1':
                    self.menu_aventura()
                elif op == '2':
                    self.menu_personagem()
                elif op == '3':
                    self.menu_loja()
                elif op == '4':
                    self.menu_sistema()
                elif op == '0':
                    print("Até logo!")
                    sys.exit()
                else:
                    print("Opção inválida.")

    # --------------------------------------------------------------
    # --- FUNÇÕES DE NAVEGAÇÃO ---
    # --------------------------------------------------------------
    
    def menu_personagem(self) -> None:
        """Menu de visualização e gerenciamento do herói."""
        if not self.personagem: return
        
        while True:
            self._mostrar_status()
            print("\n--- GERENCIAR HERÓI ---")
            print("[1] Inventário (Usar/Equipar)")
            print("[2] Descansar (Cura Total)")
            print("[3] Voltar")
            
            op = input("Escolha uma opção: ").strip()
            
            if op == '1':
                self.menu_inventario_equipamento()
            elif op == '2':
                self._descansar()
            elif op == '3':
                break
            else:
                print("Opção inválida.")

    def menu_inventario_equipamento(self) -> None:
        """Menu que lida com Inventário e Equipamento."""
        if not self.personagem: return
        
        while True:
            self.personagem.inventario.listar_itens()
            print("\n=== INVENTÁRIO & EQUIPAMENTO ===")
            print("[1] Usar Consumível")
            print("[2] Equipar Item")
            print("[3] Desequipar Item")
            print("[4] Voltar")
            
            op = input("Escolha uma opção: ").strip()
            
            if op == '1':
                nome_item = input("Digite o NOME exato do item para usar: ").strip()
                self.personagem.usar_consumivel(nome_item)
            elif op == '2':
                nome_item = input("Digite o NOME exato do item para equipar: ").strip()
                self.personagem.equipar_item(nome_item)
            elif op == '3':
                slot = input("Digite o slot para desequipar (arma ou armadura): ").strip().lower()
                if slot in ["arma", "armadura"]:
                    self.personagem.desequipar_item(slot)
                else:
                    print("Slot inválido.")
            elif op == '4':
                break
            else:
                print("Opção inválida.")

    def menu_sistema(self) -> None:
        """Menu de Salvar/Carregar."""
        if not self.personagem: return
        
        while True:
            print("\n--- SISTEMA ---")
            print("[1] Salvar Jogo")
            print("[2] Carregar Jogo")
            print("[3] Voltar")
            
            op = input("Escolha uma opção: ").strip()
            
            if op == '1':
                self._salvar_jogo()
            elif op == '2':
                self._carregar_jogo_interativo()
            elif op == '3':
                break
            else:
                print("Opção inválida.")

    def _descansar(self) -> None:
        """Cura o personagem totalmente fora do combate (Opção 2 do Menu Personagem)."""
        if not self.personagem: return

        cura_valor = self.personagem.curar()
        if cura_valor > 0:
            print(f"🛌 {self.personagem.nome} descansou e se curou totalmente! HP restaurado: {cura_valor}.")
        else:
            print(f"🛡️ {self.personagem.nome} já está com a vida máxima.")
            
    # --------------------------------------------------------------
    # --- FUNÇÕES DE PERSISTÊNCIA E CARREGAMENTO (COM CORREÇÕES) ---
    # --------------------------------------------------------------

    def _carregar_jogo_interativo(self, nome_arquivo: str = "save_data.json"):
        """Permite ao usuário carregar um save existente."""
        if nome_arquivo == "save_data.json":
            if not self.repositorio.save_padrao_existe(nome_arquivo):
                 print("❌ Arquivo de save padrão não encontrado.")
                 return
        else:
             nome_arquivo = input("Digite o nome do arquivo para carregar (Ex: save_data.json): ").strip() or "save_data.json"
        
        if not self._carregar_jogo_silencioso(nome_arquivo=nome_arquivo):
             print("❌ Falha ao carregar o jogo.")

    def _carregar_jogo_silencioso(self, nome_arquivo: str = "save_data.json") -> bool:
        """Tenta carregar o save padrão ou especificado (silenciosamente).
           Inclui correções para desserialização de Atributos e Arquétipo.
        """
        dados = self.repositorio.carregar(nome_arquivo)
        if not dados:
            return False

        try:
            # 1. Tenta obter o dicionário do personagem (pode estar sob 'personagem_data' ou no root).
            p_data = dados.get('personagem_data') 
            
            # 2. Se a chave 'personagem_data' não for encontrada, assume que 'dados' é o dicionário do personagem.
            if not isinstance(p_data, dict):
                p_data = dados 
                
            # 3. Validação final da estrutura
            if not isinstance(p_data, dict) or not p_data:
                print("❌ Falha crítica: Os dados do save estão vazios ou corrompidos.")
                return False
                
            # --- CORREÇÃO DE LEITURA DO ARQUÉTIPO ---
            arquetipo = p_data.get('_arquetipo') 
            
            classes_validas = ["Guerreiro", "Mago", "Arqueiro", "Curandeiro", "Personalizado"]
            if not isinstance(arquetipo, str) or arquetipo not in classes_validas:
                print(f"❌ Erro: Arquétipo desconhecido ou inválido '{arquetipo}' no save. Confirme se a chave '_arquetipo' existe no save.")
                return False
                
            # 1. Desserializa Atributos
            atrib_data = p_data.get('_atrib', {}) 
            if not isinstance(atrib_data, dict): atrib_data = {}
            atributos = Atributos(**atrib_data) 
            
            # 2. Criação da Instância Personagem
            nome_personagem = p_data.get('_nome', 'Desconhecido')
            p = None
            
            if arquetipo == "Guerreiro":
                p = Guerreiro(nome_personagem)
            elif arquetipo == "Mago":
                p = Mago(nome_personagem)
            elif arquetipo == "Arqueiro":
                p = Arqueiro(nome_personagem)
            elif arquetipo == "Curandeiro":
                p = Curandeiro(nome_personagem)
            
            if p is None:
                # Se o arquétipo for válido, mas a criação falhou (ex: Personalizado não implementado)
                print(f"❌ Erro: Falha ao instanciar o objeto para o arquétipo '{arquetipo}'.")
                return False

            # 3. Restaura o estado e conecta os Atributos
            p._atrib = atributos 
            p.nivel = p_data.get('nivel', 1)
            p.xp = p_data.get('xp', 0)
            p.hp_atual = p_data.get('hp_atual', p._atrib.vida_max_total) 
            
            # 4. Restaura Inventário
            inventario_data = p_data.get('inventario')
            if inventario_data:
                p.inventario.moedas = inventario_data.get('moedas', 0)
                p.inventario.itens = inventario_data.get('itens', {}) 

            # 5. Restaura Equipamentos
            p.arma_equipada = None
            p.armadura_equipada = None
            
            equipados_data = []
            arma_data = p_data.get('arma_equipada')
            armadura_data = p_data.get('armadura_equipada')
            
            # Adiciona dados se forem um dicionário válido (gerado por asdict)
            if arma_data and isinstance(arma_data, dict): equipados_data.append(arma_data)
            if armadura_data and isinstance(armadura_data, dict): equipados_data.append(armadura_data)

            # Re-equipa os itens, aplicando os bônus aos atributos
            for item_data in equipados_data:
                item_obj = get_item_by_name(item_data.get('nome')) 
                if item_obj:
                    # Adiciona ao inventário para que equipar_item possa removê-lo de lá
                    p.inventario.adicionar_item(item_obj)
                    p.equipar_item(item_obj.nome)


            self.personagem = p
            print(f"\n🎉 Personagem '{p.nome}' (Nível {p.nivel}) carregado com sucesso!")
            return True
                
        except Exception as e:
            # Captura qualquer erro inesperado durante a desserialização
            print(f"❌ Erro CRÍTICO ao restaurar o objeto Personagem: {type(e).__name__}: {e}")
            self.personagem = None 
            return False

    # --------------------------------------------------------------
    # --- FUNÇÕES DE CRIAÇÃO E STATUS ---
    # --------------------------------------------------------------
    
    def _criar_personagem(self) -> None:
        """Permite ao usuário criar um novo personagem."""
        if self.personagem is not None:
             confirm = input("ATENÇÃO: Criar um novo personagem perderá o atual. Continuar? (s/n): ").strip().lower()
             if confirm != 's':
                 return
             self.repositorio.deletar_save(self._save_padrao)
             self.personagem = None 

        print("\n--- CRIAÇÃO DE PERSONAGEM ---")
        nome = input("Digite o nome do seu herói: ").strip()
        
        print("\nEscolha seu Arquétipo:")
        print("[1] Guerreiro (ATK/HP/DEF)")
        print("[2] Mago (Dano/MP)")
        print("[3] Arqueiro (ATK/Agilidade)")
        print("[4] Curandeiro (Cura/MP)")
        
        while True:
            escolha = input("Opção (1-4): ").strip()
            if escolha == '1':
                self.personagem = Guerreiro(nome)
                break
            elif escolha == '2':
                self.personagem = Mago(nome)
                break
            elif escolha == '3':
                self.personagem = Arqueiro(nome)
                break
            elif escolha == '4':
                self.personagem = Curandeiro(nome)
                break
            else:
                print("Escolha inválida.")
        
        if self.personagem:
            print(f"\n✅ {self.personagem.nome}, o {self.personagem.arquetipo}, está pronto para a aventura!")
            self._salvar_jogo() # Salva automaticamente o novo personagem


    def _mostrar_status(self) -> None:
        """Exibe o status completo do personagem."""
        if not self.personagem:
            print("Nenhum personagem carregado.")
            return

        p = self.personagem
        atrib = p.atrib

        print("\n--- STATUS DO HERÓI ---")
        print(f"👤 Nome: {p.nome} ({p.arquetipo})")
        print(p.barra_xp(largura=30))
        print(f"❤️ HP: {p.hp_atual}/{atrib.vida_max_total} | 💧 MP: {atrib.mana}/{atrib.mana_max_total}")
        print(f"⚔️ ATK (Total): {atrib.ataque_total} (Base: {atrib.ataque} + Equip: {atrib._ataque_eq})")
        print(f"🛡️ DEF (Total): {atrib.defesa_total} (Base: {atrib.defesa} + Equip: {atrib._defesa_eq})")
        
        # Equipamentos
        arma = p.arma_equipada.nome if p.arma_equipada else "Nenhuma"
        armadura = p.armadura_equipada.nome if p.armadura_equipada else "Nenhuma"
        print(f"🔧 Arma: {arma} | Armadura: {armadura}")
        
        p.inventario.listar_itens()


    def _salvar_jogo(self):
        """Salva o estado atual do Personagem."""
        if self.personagem:
            if self.personagem.hp_atual <= 0:
                print("❌ Não é possível salvar um personagem nocauteado! Cure-se primeiro.")
                return
                
            # O to_dict do Personagem gera o dicionário do herói
            dados_personagem_raw = self.personagem.to_dict() 
            
            # Empacota os dados para o Repositório (assumindo que Repositório espera uma chave principal)
            dados_para_salvar = {'personagem_data': dados_personagem_raw} 

            if dados_para_salvar:
                 self.repositorio.salvar(self._save_padrao, dados_para_salvar)
                 print(f"✔ Jogo salvo com sucesso em '{self._save_padrao}'.")
            else:
                 print("❌ Falha na serialização dos dados do personagem.")
        else:
            print("❌ Nenhuma personagem para salvar.")

    # --------------------------------------------------------------
    # --- FUNÇÕES DE LOJA ---
    # --------------------------------------------------------------

    def menu_loja(self):
        """Menu principal da loja."""
        if not self.personagem: return
        while True:
            print("\n--- LOJA DO FERREIRO ---")
            print(f"Seu saldo atual: {self.personagem.inventario.moedas} moedas.")
            print("[1] Comprar Consumíveis")
            print("[2] Vender Itens")
            print("[3] Voltar")
            
            op = input("Escolha uma opção: ").strip()
            
            if op == '1':
                self._comprar_item()
            elif op == '2':
                self._vender_item()
            elif op == '3':
                break
            else:
                print("Opção inválida.")
                
    def _listar_itens_loja(self):
        """Lista os itens consumíveis que a loja vende e seus preços."""
        print("\n--- ITENS À VENDA (CONSUMÍVEIS) ---")
        for i, item_nome in enumerate(ITENS_LOJA_CONSUMIVEIS):
            item = get_item_by_name(item_nome)
            if item:
                print(f"[{i+1}] {item.nome} ({item.descricao}) | Preço: {item.valor} moedas")
        print("-------------------------------------")

    def _comprar_item(self):
        """Lógica para comprar itens consumíveis da loja."""
        if not self.personagem: return
        self._listar_itens_loja()
        
        try:
            escolha = input("Digite o NÚMERO do item para comprar, ou 0 para voltar: ").strip()
            if escolha == '0': return
            
            idx = int(escolha) - 1
            if 0 <= idx < len(ITENS_LOJA_CONSUMIVEIS):
                item_nome = ITENS_LOJA_CONSUMIVEIS[idx]
                item_obj = get_item_by_name(item_nome)
                
                if item_obj:
                    if self.personagem.inventario.moedas >= item_obj.valor:
                        self.personagem.inventario.moedas -= item_obj.valor
                        self.personagem.inventario.adicionar_item(item_obj, 1)
                        print(f"✔ Você comprou {item_nome} por {item_obj.valor} moedas.")
                    else:
                        print("❌ Moedas insuficientes.")
                else:
                    print("Item não encontrado ou inválido.")
            else:
                print("Escolha inválida.")
        except ValueError:
            print("Entrada inválida.")
            
    def _vender_item(self):
        """Lógica para vender itens do inventário."""
        if not self.personagem: return
        self.personagem.inventario.listar_itens()
        
        item_nome = input("Digite o NOME exato do item para vender (ou 0 para voltar): ").strip()
        if item_nome == '0': return
        
        item_obj = self.personagem.inventario.get_item(item_nome)
        
        if not item_obj:
            print(f"❌ Item '{item_nome}' não encontrado no seu inventário.")
            return

        is_equipped = (self.personagem.arma_equipada is not None and item_obj.nome == self.personagem.arma_equipada.nome) or \
                      (self.personagem.armadura_equipada is not None and item_obj.nome == self.personagem.armadura_equipada.nome)

        if is_equipped:
            print("❌ Desequipe o item antes de vendê-lo.")
            return

        valor_venda = item_obj.valor // 2 
        
        if self.personagem.inventario.remover_item(item_nome, 1):
            self.personagem.inventario.moedas += valor_venda
            print(f"✔ Você vendeu {item_nome} por {valor_venda} moedas.")
        else:
            print("❌ Não foi possível vender o item.")

    # --------------------------------------------------------------
    # --- FUNÇÕES DE AVENTURA ---
    # --------------------------------------------------------------
                
    def menu_aventura(self) -> None:
        """Menu de configuração e início da aventura."""
        while self.personagem is not None:
            
            cenarios = list(INIMIGOS_TABLE.keys())
            dificuldades = ["Fácil", "Média", "Difícil"]
            
            while True:
                if self.personagem is None: 
                    return

                print("\n--- CONFIGURAR AVENTURA ---")
                
                print(f"Cenário Atual: {self.missao_config['cenario']}")
                print(f"Dificuldade Atual: {self.missao_config['dificuldade']}")
                
                print("\n[1] Escolher Cenário")
                print("[2] Escolher Dificuldade")
                print("[3] Iniciar Missão (Encontro Aleatório)")
                print("[4] Voltar")
                
                op = input("Escolha uma opção: ").strip()
                
                if op == '1':
                    print("\n--- CENÁRIOS DISPONÍVEIS ---")
                    for i, c in enumerate(cenarios):
                        print(f"[{i+1}] {c}")
                    
                    escolha_c = input("Escolha o número do cenário: ").strip()
                    if escolha_c.isdigit() and 1 <= int(escolha_c) <= len(cenarios):
                        self.missao_config['cenario'] = cenarios[int(escolha_c) - 1]
                        print(f"✅ Cenário alterado para: {self.missao_config['cenario']}")
                    else:
                        print("Escolha inválida.")
                        
                elif op == '2':
                    print("\n--- DIFICULDADES ---")
                    for i, d in enumerate(dificuldades):
                        print(f"[{i+1}] {d}")
                    
                    escolha_d = input("Escolha o número da dificuldade: ").strip()
                    if escolha_d.isdigit() and 1 <= int(escolha_d) <= len(dificuldades):
                        self.missao_config['dificuldade'] = dificuldades[int(escolha_d) - 1]
                        print(f"✅ Dificuldade alterada para: {self.missao_config['dificuldade']}")
                    else:
                        print("Escolha inválida.")
                        
                elif op == '3':
                    if self.personagem.hp_atual <= 0:
                         print("❌ Seu herói está nocauteado! Use a opção 'Descansar' para curar-se.")
                         continue

                    inimigo = self.rolar_boss_fight(self.missao_config['dificuldade'])
                    
                    dificuldade_missao = 'Boss' if hasattr(inimigo, 'item_drop_garantido') else self.missao_config['dificuldade']
                    
                    self.simular_missao(inimigo, dificuldade_missao)
                    
                    if self.personagem is None:
                         return

                elif op == '4':
                    return
                
                else:
                    print("Opção inválida.")
        
        return


    def simular_missao(self, inimigo: Inimigo, dificuldade: str) -> None:
        """Inicia e executa a missão de combate."""
        if not self.personagem: return
        
        missao = Missao(f"Batalha contra {inimigo.nome}", inimigo)
        
        resultado = missao.executar(self.personagem, dificuldade=dificuldade)
        
        print("\n--- FIM DA MISSÃO ---")
        print(f"Resultado: {'Vitória!' if resultado.venceu else 'Derrota!'}")
        print(f"XP Ganho: {resultado.xp_ganho}")
        
        if not resultado.venceu and self.personagem.hp_atual == 0:
            print("\n=============================================")
            print(f"💀 MORTE PERMANENTE! {self.personagem.nome} caiu em batalha.")
            print("Seu save será DELETADO. O herói não pode ser recuperado.")
            print("=============================================")
            
            self.repositorio.deletar_save(self._save_padrao)
            self.personagem = None 
            
        elif not resultado.venceu:
             self.personagem.hp_atual = self.personagem.hp_atual if self.personagem.hp_atual > 0 else 0


    def rolar_boss_fight(self, dificuldade: str) -> Inimigo:
        """Rola um dado para ver se um Inimigo Comum ou um Chefe é gerado."""
        chance_boss = 0
        if dificuldade == "Média":
            chance_boss = 5
        elif dificuldade == "Difícil":
            chance_boss = 15
            
        rolagem = random.randint(1, 100)
        
        if rolagem <= chance_boss:
            boss = self.gerar_boss()
            if boss:
                return boss
        
        return self.gerar_inimigo()

    def gerar_boss(self) -> Inimigo | None:
        """Gera o Chefe (Boss) específico do cenário atual, com drop garantido."""
        cenario = self.missao_config['cenario']
        boss_data = BOSS_TABLE.get(cenario)
        
        if not boss_data:
            print(f"❌ Não há um Chefe definido para o cenário: {cenario}.")
            return None
        
        nome, vida, ataque, defesa, item_drop_nome = boss_data
        
        boss = Inimigo(
            nome=nome, 
            vida=vida, 
            ataque=ataque, 
            defesa=defesa, 
        )
        setattr(boss, 'item_drop_garantido', item_drop_nome)
        setattr(boss, 'xp_recompensa', 500)
        
        print(f"\n📢 Você encontrou o Chefe: {nome}! Prepare-se para a batalha!")
        return boss

    def gerar_inimigo(self) -> Inimigo:
        """Gera um inimigo aleatório baseado no cenário atual e na dificuldade."""
        cenario = self.missao_config['cenario']
        lista_inimigos = INIMIGOS_TABLE.get(cenario, INIMIGOS_TABLE["Floresta Sombria"])
        
        nome, vida, ataque, defesa = random.choice(lista_inimigos)
        
        # Ajuste de Dificuldade
        multiplicador = 1.0
        if self.missao_config['dificuldade'] == "Média":
            multiplicador = 1.5
        elif self.missao_config['dificuldade'] == "Difícil":
            multiplicador = 2.0
            
        vida = int(vida * multiplicador)
        ataque = int(ataque * multiplicador)
        defesa = int(defesa * multiplicador) 
        
        return Inimigo(nome, vida, ataque, defesa)