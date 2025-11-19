class Inventario:
    def __init__(self, limite_itens: int = 20):
        self.limite_itens = limite_itens
        self.itens = []  # lista de Equipamento, Poções, etc.

    def adicionar(self, item) -> bool:
        """Adiciona um item ao inventário se houver espaço."""
        if len(self.itens) >= self.limite_itens:
            print("Inventário cheio! Não é possível adicionar o item.")
            return False
        
        self.itens.append(item)
        print(f"👜 Item adicionado ao inventário: {item}")
        return True

    def remover(self, item) -> bool:
        """Remove um item se ele existir no inventário."""
        if item in self.itens:
            self.itens.remove(item)
            print(f"❌ Item removido do inventário: {item}")
            return True
        
        print("⚠ O item não está no inventário.")
        return False

    def listar(self):
        """Mostra todos os itens no inventário."""
        if not self.itens:
            print("📦 Inventário vazio.")
            return
        
        print("\n=== INVENTÁRIO ===")
        for i, item in enumerate(self.itens, start=1):
            print(f"{i}. {item}")
        print("===================\n")

    def pegar_item_por_indice(self, indice: int):
        """Retorna o item pelo índice (1 baseado)."""
        if 1 <= indice <= len(self.itens):
            return self.itens[indice - 1]

        print("⚠ Índice inválido!")
        return None
    




class InventarioController:

    def __init__(self, personagem):
        self.personagem = personagem

    def listar(self):
        self.personagem.inventario.listar()

    def equipar_por_indice(self, indice: int):
        inventario = self.personagem.inventario
        item = inventario.pegar_item_por_indice(indice)

        if not item:
            print("Item inválido.")
            return False

        if self.personagem.equipar(item):
            inventario.remover(item)
            return True

        return False

    def desequipar_arma(self):
        self.personagem.desequipar("arma")

    def desequipar_armadura(self):
        self.personagem.desequipar("armadura")