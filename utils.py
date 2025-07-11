import os

def limpar_terminal():
    """Limpa o console."""
    os.system('cls' if os.name == 'nt' else 'clear')

def pausar_e_limpar():
    """Aguarda um Enter e limpa o console."""
    input("\nPressione Enter para continuar...")
    limpar_terminal()