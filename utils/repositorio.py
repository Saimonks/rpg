from __future__ import annotations
import json
import os
from typing import Any


class Repositorio:

    def __init__(self, pasta_saves: str = "saves"):
        self.pasta_saves = pasta_saves
        os.makedirs(self.pasta_saves, exist_ok=True)

    # Caminho completo do arquivo
    def _caminho(self, nome_arquivo: str) -> str:
        return os.path.join(self.pasta_saves, nome_arquivo)

    def salvar(self, nome_arquivo: str, dados: dict[str, Any]) -> None:
        try:
            caminho = self._caminho(nome_arquivo)
            with open(caminho, "w", encoding="utf-8") as arq:
                json.dump(dados, arq, indent=4, ensure_ascii=False)
            print(f"✔ Jogo salvo em: {caminho}")
        except Exception as e:
            print(f"❌ Erro ao salvar arquivo: {e}")

    def carregar(self, nome_arquivo: str) -> dict[str, Any] | None:
        try:
            caminho = self._caminho(nome_arquivo)
            if not os.path.exists(caminho):
                print("❌ Arquivo de save não encontrado.")
                return None

            with open(caminho, "r", encoding="utf-8") as arq:
                dados = json.load(arq)

            print(f"✔ Save carregado: {caminho}")
            return dados

        except Exception as e:
            print(f"❌ Erro ao carregar arquivo: {e}")
            return None
