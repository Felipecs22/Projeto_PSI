import os
import hashlib

def limpar_terminal():
    """Limpa o console."""
    os.system('cls' if os.name == 'nt' else 'clear')

def pausar_e_limpar():
    """Aguarda um Enter e limpa o console."""
    input("\nPressione Enter para continuar...")
    limpar_terminal()

def gerar_hash_senha(senha: str) -> str:
    """gera um hash SHA-256 para uma senha fornecida."""
    senha_em_bytes = senha.encode('utf-8')
    
    # cria o objeto hash usando o algoritmo SHA-256
    hash_obj = hashlib.sha256(senha_em_bytes)
    
    # .hexdigest() converte o resultado em uma string hexadecimal legível
    return hash_obj.hexdigest()