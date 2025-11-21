from __future__ import annotations
from jogo import Jogo
import sys 

def menu() -> None:
    """Função de inicialização do aplicativo."""
    jogo = Jogo()
    # Chama o método principal de navegação. 
    jogo.menu_principal() 


if __name__ == "__main__":
    menu()