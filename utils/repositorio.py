import json
import os
from typing import Any

class Repositorio:
    """
    Gerencia a persistência de dados (Save e Load) usando arquivos JSON.
    Todos os saves são armazenados no diretório 'saves/'.
    """

    def __init__(self, pasta_saves: str = "saves") -> None:
        self.pasta_saves = pasta_saves
        self._inicializar_pasta()

    def _inicializar_pasta(self) -> None:
        """
        Garante que o diretório 'saves' exista.
        """
        if not os.path.exists(self.pasta_saves):
            os.makedirs(self.pasta_saves)
            print(f"Diretório '{self.pasta_saves}' criado com sucesso.")

    def _obter_caminho_completo(self, nome_arquivo: str) -> str:
        """
        Retorna o caminho completo para o arquivo de save.
        """
        return os.path.join(self.pasta_saves, nome_arquivo)

    def salvar(self, nome_arquivo: str, dados: dict) -> bool:
        """
        Salva o dicionário 'dados' no arquivo especificado em formato JSON.
        """
        caminho = self._obter_caminho_completo(nome_arquivo)
        try:
            with open(caminho, 'w', encoding='utf-8') as f:
                # O indent=4 serve apenas para facilitar a leitura humana do arquivo
                json.dump(dados, f, indent=4) 
            print(f"✔ Jogo salvo com sucesso em: {caminho}")
            return True
        except TypeError as e:
            print(f"❌ Erro ao salvar arquivo: {e}")
            print("Dica: Certifique-se de usar .to_dict() em objetos complexos (como Atributos) antes de salvar.")
            return False
        except Exception as e:
            print(f"❌ Erro desconhecido ao salvar o arquivo: {e}")
            return False

    def carregar(self, nome_arquivo: str) -> dict[str, Any] | None:
        """
        Carrega os dados do arquivo especificado. Retorna um dicionário ou None em caso de falha.
        """
        caminho = self._obter_caminho_completo(nome_arquivo)
        if not os.path.exists(caminho):
            print(f"❌ Erro: Arquivo de save não encontrado em: {caminho}")
            return None
        
        try:
            with open(caminho, 'r', encoding='utf-8') as f:
                dados = json.load(f)
            print(f"✔ Jogo carregado com sucesso de: {caminho}")
            return dados
        except json.JSONDecodeError:
            print(f"❌ Erro ao decodificar JSON. Arquivo '{nome_arquivo}' pode estar corrompido.")
            return None
        except Exception as e:
            print(f"❌ Erro desconhecido ao carregar o arquivo: {e}")
            return None

# --- Exemplo de uso (Opcional, apenas para testes) ---
# if __name__ == "__main__":
#     repo = Repositorio()
#     dados_teste = {"nivel": 5, "xp": 120, "nome": "Testador"}
#     repo.salvar("teste_save.json", dados_teste)
#     dados_carregados = repo.carregar("teste_save.json")
#     print(f"Carregado: {dados_carregados}")