from __future__ import annotations
import json
import os
from typing import Any, Dict


class Repositorio:
    """
    Gerencia a persistência de dados (Save e Load) usando arquivos JSON.
    Todos os saves são armazenados no diretório 'saves/' (Tarefa T7).
    """

    def __init__(self, pasta_saves: str = "saves"):
        self.pasta_saves = pasta_saves
        self._inicializar_pasta()

    def _inicializar_pasta(self) -> None:
        """Garante que o diretório 'saves' exista."""
        if not os.path.exists(self.pasta_saves):
            os.makedirs(self.pasta_saves)
            print(f"Diretório '{self.pasta_saves}' criado com sucesso.")

    def _obter_caminho_completo(self, nome_arquivo: str) -> str:
        """Retorna o caminho completo para o arquivo."""
        return os.path.join(self.pasta_saves, nome_arquivo)

    def salvar(self, nome_arquivo: str, dados: dict) -> None:
        """Salva o dicionário 'dados' no arquivo especificado em formato JSON."""
        caminho = self._obter_caminho_completo(nome_arquivo)
        try:
            with open(caminho, 'w', encoding='utf-8') as f:
                json.dump(dados, f, indent=4, ensure_ascii=False) 
            print(f"✔ Jogo salvo com sucesso em: {caminho}")
        except Exception as e:
            print(f"❌ Erro ao salvar arquivo: {e}")

    def carregar(self, nome_arquivo: str) -> Dict[str, Any] | None:
        """Carrega os dados do arquivo especificado. Retorna um dicionário ou None."""
        caminho = self._obter_caminho_completo(nome_arquivo)
        if not os.path.exists(caminho):
            print("❌ Arquivo de save não encontrado.")
            return None
        
        try:
            with open(caminho, 'r', encoding='utf-8') as f:
                dados = json.load(f)
            print(f"✔ Save carregado: {caminho}")
            return dados
        except json.JSONDecodeError:
            print(f"❌ Erro ao decodificar JSON. Arquivo '{nome_arquivo}' pode estar corrompido.")
            return None
        except Exception as e:
            print(f"❌ Erro desconhecido ao carregar o arquivo: {e}")
            return None

    def deletar_save(self, nome_arquivo: str) -> bool:
        """Deleta o arquivo de save permanentemente (Usado para Permadeath)."""
        caminho = self._obter_caminho_completo(nome_arquivo)
        if os.path.exists(caminho):
            try:
                os.remove(caminho)
                print(f"🗑️ Save deletado permanentemente: {nome_arquivo}")
                return True
            except Exception as e:
                print(f"❌ Erro ao deletar save: {e}")
                return False
        return False