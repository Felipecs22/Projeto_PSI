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
    """Gera um hash SHA-256 para uma senha fornecida."""
    # .encode('utf-8') converte a string em bytes, que é o que o hash precisa
    senha_em_bytes = senha.encode('utf-8')
    
    # Cria o objeto hash usando o algoritmo SHA-256
    hash_obj = hashlib.sha256(senha_em_bytes)
    
    # .hexdigest() converte o resultado em uma string hexadecimal legível
    return hash_obj.hexdigest()