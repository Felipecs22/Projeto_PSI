import sqlite3
from models import Usuario
NOME_BANCO = "investimatch.db"

def inicializar_db():
    """
    Cria as tabelas do banco de dados se elas não existirem.
    Esta função deve ser chamada uma vez no início da execução do programa.
    """
    print("Inicializando banco de dados...")
    
    conexao = sqlite3.connect(NOME_BANCO)
    cursor = conexao.cursor()
    try:
        # Tabela de usuários
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            senha_hash TEXT NOT NULL
        )
        """)

        # Tabela de perfis de investidor
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS perfis (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER NOT NULL,
            tolerancia_risco INTEGER,
            experiencia INTEGER,
            necessidade_liquidez INTEGER,
            FOREIGN KEY (usuario_id) REFERENCES usuarios (id)
        )
        """)
        
        # Tabela para guardar os investimentos feitos pelo usuário
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS investimentos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER NOT NULL,
            nome_ativo TEXT NOT NULL,
            valor_aportado REAL NOT NULL,
            data_aporte TEXT NOT NULL,
            FOREIGN KEY (usuario_id) REFERENCES usuarios (id)
        )
        """)

        conexao.commit()
        print("Banco de dados inicializado com sucesso.")
    finally:
        conexao.close()


def adicionar_usuario(usuario: object):
    """Adiciona um novo objeto Usuario ao banco de dados."""
    conexao = sqlite3.connect(NOME_BANCO)
    cursor = conexao.cursor()
    try:
        cursor.execute(
            "INSERT INTO usuarios (email, senha_hash) VALUES (?, ?)",
            (usuario.email, usuario.senha) # Usamos '?' para evitar SQL Injection
        )
        conexao.commit()
        print(f"Usuário {usuario.email} adicionado com sucesso.")
    finally:
        conexao.close()

def verificar_email_existe(email: str) -> bool:
    """Verifica se um e-mail já está cadastrado no banco."""
    conexao = sqlite3.connect(NOME_BANCO)
    cursor = conexao.cursor()
    try:
        cursor.execute("SELECT id FROM usuarios WHERE email = ?", (email,))
        resultado = cursor.fetchone() # Pega o primeiro resultado
        return resultado is not None # Retorna True se encontrou algo, False caso contrário
    finally:
        conexao.close()

def buscar_usuario_por_email(email: str) -> Usuario | None:
    """
    Busca um usuário pelo seu e-mail no banco de dados.
    Retorna um objeto Usuario completo se encontrar, caso contrário, retorna None.
    """
    conexao = sqlite3.connect(NOME_BANCO)
    cursor = conexao.cursor()
    try:
        # Selecionamos todas as colunas necessárias para reconstruir o objeto
        cursor.execute("SELECT id, email, senha_hash FROM usuarios WHERE email = ?", (email,))
        resultado = cursor.fetchone()  # Pega a primeira (e única) linha correspondente

        if resultado:
            # 'resultado' é uma tupla, ex: (1, 'teste@email.com', '123')
            # Nós a desempacotamos para criar um objeto Usuario
            id_usuario, email_usuario, senha_usuario = resultado
            return Usuario(id=id_usuario, email=email_usuario, senha=senha_usuario)
        
        # Retorna None se o cursor.fetchone() não encontrou nenhum usuário
        return None
    finally:
        conexao.close()