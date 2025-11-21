from __future__ import annotations
from jogo import Jogo
import sys # Necessário para sair do jogo

def menu() -> None:
    """Função de inicialização do aplicativo."""
    jogo = Jogo()
    # Chama o método principal de navegação. 
    # (Este método contém o loop "while True" na classe Jogo.)
    jogo.menu_principal() 


if __name__ == "__main__":
    menu()