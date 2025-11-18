from __future__ import annotations
from models.inimigo import Inimigo 
from models.missao import Missao 
from models.personagem import Personagem 
from models.classes import Guerreiro, Mago
from models.base import Atributos # Necessário para a desserialização (Carregar)
from utils.repositorio import Repositorio # Necessário para Save/Load


class Jogo:

    def __init__(self) -> None:
        # Inicializa como Dicionário para ter as chaves 'nome' e 'arquetipo' para os menus.
        self.personagem: Personagem | dict = {"nome": None, "arquetipo": None}
        self.missao_config = {
            "dificuldade": "Fácil", 
            "cenario": "Trilha",
        }
        self._ultimo_save = None
        self._ultimo_load = None
        self.repositorio = Repositorio()

    def menu_criar_personagem(self) -> None:
        while True:
            print("\n=== Criar Personagem ===")
            
            if isinstance(self.personagem, Personagem):
                nome_atual = self.personagem.nome
                arq_atual = self.personagem._arquetipo
            else:
                nome_atual = self.personagem.get('nome', '(não definido)') if self.personagem else '(não definido)'
                arq_atual = self.personagem.get('arquetipo', '(não definido)') if self.personagem else '(não definido)'
            
            print(f"Personagem atual: {nome_atual} ({arq_atual})")
            print("[1] Definir nome")
            print("[2] Escolher arquétipo")
            print("[3] Confirmar criação")
            print("[9] Ajuda")
            print("[0] Voltar")
            op = input("> ").strip()

            if op == "1":
                self._definir_nome()
            elif op == "2":
                self._escolher_arquetipo()
            elif op == "3":
                self._confirmar_criacao()
            elif op == "9":
                self._ajuda_criar_personagem()
            elif op == "0":
                break
            else:
                print("Opção inválida.")

    def _definir_nome(self) -> None:
        nome = input("Digite o nome do personagem: ").strip()
        if nome:
            if isinstance(self.personagem, Personagem):
                self.personagem._nome = nome
            else:
                self.personagem["nome"] = nome
            print(f"Nome definido: {nome}")
        else:
            print("Nome não alterado.")

    def _escolher_arquetipo(self) -> None:
        print("\nArquétipos disponíveis:")
        print("[1] Guerreiro")
        print("[2] Mago")
        print("[3] Arqueiro (Em Breve)")
        print("[4] Curandeiro (Em Breve)")
        print("[5] Personalizado (Em Breve)")
        escolha = input("> ").strip()

        mapa = {
            "1": "Guerreiro",
            "2": "Mago",
            "3": "Arqueiro",
            "4": "Curandeiro",
            "5": "Personalizado",
        }
        arq = mapa.get(escolha)
        if arq:
            if isinstance(self.personagem, Personagem):
                 self.personagem = {"nome": self.personagem.nome, "arquetipo": arq}
            else:
                 self.personagem["arquetipo"] = arq
            print(f"Arquétipo definido: {arq}")
        else:
            print("Opção inválida. Arquétipo não alterado.")

    def _confirmar_criacao(self) -> None:
        """ Cria a instância real do Personagem (Guerreiro/Mago). """
        if not isinstance(self.personagem, dict):
            print("Personagem já criado. Use a opção 'Carregar' para reconfigurar.")
            return

        nome = self.personagem.get("nome")
        arquetipo = self.personagem.get("arquetipo")
        
        if not nome or not arquetipo:
            print("Defina um nome e um arquétipo antes de confirmar a criação.")
            return

        if arquetipo == "Guerreiro":
            self.personagem = Guerreiro(nome)
        elif arquetipo == "Mago":
            self.personagem = Mago(nome)
        else:
            print("Arquétipo não implementado (escolha Guerreiro ou Mago).")
            return

        print(f"\nPersonagem {arquetipo} criado: {self.personagem.nome}!")
        print(f"HP inicial: {self.personagem.hp_atual}/{self.personagem._atrib.vida_max}")
        print(f"Mana inicial: {self.personagem.atrib.mana}/{self.personagem._atrib.mana_max}")
        print(f"ataque: {self.personagem.atrib.ataque}")
        print(f"defesa: {self.personagem.atrib.defesa}")
        print(f"Arma: {self.personagem.arma.nome} ({self.personagem.arma.raridade.name})")

    def _ajuda_criar_personagem(self) -> None:
        print("\nAjuda — Criar Personagem")
        print("- Defina um nome e um arquétipo para continuar.")
        print("- Esta etapa não cria atributos reais; é apenas o fluxo do menu.")
        print("- Implementações futuras podem usar essas escolhas para gerar status.")

    def menu_missao(self) -> None:
        while True:
            print("\n=== Missão ===")
            print(f"Dificuldade atual: {self.missao_config['dificuldade']}")
            print(f"Cenário atual:     {self.missao_config['cenario']}")
            print("[1] Escolher dificuldade")
            print("[2] Escolher cenário")
            print("[3] Pré-visualizar missão")
            print("[4] Iniciar missão")
            print("[9] Ajuda")
            print("[0] Voltar")
            op = input("> ").strip()

            if op == "1":
                self._escolher_dificuldade()
            elif op == "2":
                self._escolher_cenario()
            elif op == "3":
                self._preview_missao()
            elif op == "4":
                self._iniciar_missao_placeholder()
            elif op == "9":
                self._ajuda_missao()
            elif op == "0":
                break
            else:
                print("Opção inválida.")

    def _escolher_dificuldade(self) -> None:
        print("\nDificuldades:")
        print("[1] Fácil")
        print("[2] Média")
        print("[3] Difícil")
        op = input("> ").strip()
        mapa = {"1": "Fácil", "2": "Média", "3": "Difícil"}
        dif = mapa.get(op)
        if dif:
            self.missao_config["dificuldade"] = dif
            print(f"Dificuldade definida: {dif}")
        else:
            print("Opção inválida.")

    def _escolher_cenario(self) -> None:
        print("\nCenários:")
        print("[1] Trilha")
        print("[2] Floresta")
        print("[3] Caverna")
        print("[4] Ruínas")
        op = input("> ").strip()
        mapa = {"1": "Trilha", "2": "Floresta", "3": "Caverna", "4": "Ruínas"}
        cen = mapa.get(op)
        if cen:
            self.missao_config["cenario"] = cen
            print(f"Cenário definido: {cen}")
        else:
            print("Opção inválida.")

    def _preview_missao(self) -> None:
        print("\nPré-visualização da Missão")
        print(f"- Dificuldade: {self.missao_config['dificuldade']}")
        print(f"- Cenário:     {self.missao_config['cenario']}")
        print("- Inimigos e recompensas: (em breve)")
        print("- Regras de combate: (em breve)")

    def gerar_inimigo(self) -> Inimigo:
        dificuldade = self.missao_config["dificuldade"]
        tabela = {
            "Fácil": {"vida": 30, "ataque": 5, "defesa": 2}, 
            "Média": {"vida": 50, "ataque": 10, "defesa": 5}, 
            "Difícil": {"vida": 80, "ataque": 16, "defesa": 8},
        }

        config = tabela.get(dificuldade, tabela["Fácil"])
        nome_inimigo = {
            "Trilha": "Lobo selvagem",
            "Floresta": "Vingador da Natureza",
            "Caverna": "Morcego gigante",
            "Ruínas": "Guardião antigo",
        }.get(self.missao_config["cenario"], "Criatura Hostil")

        inimigo = Inimigo(
            nome=nome_inimigo,
            vida=config["vida"],
            ataque=config["ataque"],
            defesa=config["defesa"],
        )
        return inimigo

    def _iniciar_missao_placeholder(self) -> None:
        """ Inicia o loop de combate real na Missão. """
        if not isinstance(self.personagem, Personagem):
            print("Crie um personagem ANTES de iniciar uma missão.")
            return
        
        print("\n======================================")
        print("      PREPARANDO PARA O COMBATE...    ")
        print("======================================")

        inimigo_encontrado = self.gerar_inimigo()
        titulo_missao = f"Encontro na {self.missao_config['cenario']} ({self.missao_config['dificuldade']})"
        missao = Missao(titulo_missao, inimigo_encontrado)

        resultado = missao.executar(self.personagem) 

        print("\n=== FIM DA MISSÃO ===")
        if resultado.venceu:
            print(f"🏆 {resultado.detalhes} Você ganhou {resultado.xp_ganho} de XP!")
        else:
            print(f"💔 {resultado.detalhes} Seu personagem está fora de combate.")

        print("\nVoltando ao Menu Principal...")

    def _ajuda_missao(self) -> None:
        print("\nAjuda — Missão")

    def menu_salvar(self) -> None:
        while True:
            print("\n=== Salvar ===")
            print("[1] Salvar rápido")
            print("[2] Salvar com nome")
            print("[9] Ajuda")
            print("[0] Voltar")
            op = input("> ").strip()

            if op == "1":
                self._salvar_rapido()
            elif op == "2":
                self._salvar_nomeado()
            elif op == "9":
                self._ajuda_salvar()
            elif op == "0":
                break
            else:
                print("Opção inválida.")

    def _salvar_rapido(self) -> None:
        if isinstance(self.personagem, Personagem):
            dados_para_salvar = {
                "personagem_data": self.personagem.to_dict(), 
                "arquetipo": self.personagem._arquetipo,
                "missao_config": self.missao_config,
            }
            nome_arquivo = "quick_save.json"
            self.repositorio.salvar(nome_arquivo, dados_para_salvar)
            self._ultimo_save = nome_arquivo
        else:
            print("❌ Crie um personagem antes de salvar.")

    def _salvar_nomeado(self) -> None:
        """ TAREFA T8: Implementação real do salvar nomeado. """
        if isinstance(self.personagem, Personagem):
            nome = input("Nome do arquivo de save (ex.: meu_jogo.json): ").strip() or "save.json"
            # Usa to_dict() para serializar o Personagem
            dados_para_salvar = {
                "personagem_data": self.personagem.to_dict(), 
                "arquetipo": self.personagem._arquetipo,
                "missao_config": self.missao_config,
            }
            self.repositorio.salvar(nome, dados_para_salvar)
            self._ultimo_save = nome
        else:
            print("❌ Crie um personagem antes de salvar.")

    def _ajuda_salvar(self) -> None:
        print("\nAjuda — Salvar")
        print("- O save real usa a pasta 'saves' e armazena o estado atual do Personagem.")
        print("- 'Salvar rápido' usa o último nome de arquivo.")

    def menu_carregar(self) -> None:
        while True:
            print("\n=== Carregar ===")
            print("[1] Carregar último save")
            print("[2] Carregar por nome")
            print("[9] Ajuda")
            print("[0] Voltar")
            op = input("> ").strip()

            if op == "1":
                self._carregar_ultimo()
            elif op == "2":
                self._carregar_nomeado()
            elif op == "9":
                self._ajuda_carregar()
            elif op == "0":
                break
            else:
                print("Opção inválida.")

    def _carregar_ultimo(self) -> None:
        """ TAREFA T8: Implementação real do carregar último save. """
        if self._ultimo_save:
            # Chama a função de carregar nomeado com o último nome salvo
            self._carregar_nomeado(self._ultimo_save) 
        else:
            print("Nenhum save recente encontrado.")

    def _carregar_nomeado(self, nome_arquivo: str | None = None) -> None:
        """ TAREFA T8: Implementação real do carregar por nome. """
        if nome_arquivo is None:
            nome_arquivo = input("Nome do arquivo para carregar (ex.: meu_jogo.json): ").strip()

        if nome_arquivo:
            dados = self.repositorio.carregar(nome_arquivo)
            if dados:
                arquetipo = dados.get('arquetipo')
                personagem_data = dados.get('personagem_data')

                # Desserialização: Cria a instância correta (Guerreiro ou Mago)
                if arquetipo == "Guerreiro":
                    temp_personagem = Guerreiro(personagem_data['_nome'])
                elif arquetipo == "Mago":
                    temp_personagem = Mago(personagem_data['_nome'])
                else:
                    print("❌ Arquétipo desconhecido no save.")
                    return

                # 1. Desserializa o objeto Atributos
                atrib_data = personagem_data.pop('_atrib')
                atrib_instance = Atributos(**atrib_data)
                
                # 2. Atualiza o objeto Personagem com os dados restantes (HP, XP, Nível)
                temp_personagem.__dict__.update(personagem_data)
                
                # 3. Reconecta o objeto Atributos desserializado
                temp_personagem._atrib = atrib_instance
                
                self.personagem = temp_personagem
                self.missao_config = dados.get('missao_config', self.missao_config)
                self._ultimo_load = nome_arquivo
                self._ultimo_save = nome_arquivo # Atualiza o último save
                
                print(f"✔ Personagem {self.personagem.nome} ({self.personagem._arquetipo}) carregado com sucesso!")
        else:
            print("Nome do arquivo não informado.")

    def _ajuda_carregar(self) -> None:
        print("\nAjuda — Carregar")
        print("- Carregar restaura o Personagem e o último save usado.")