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

def salvar_ou_atualizar_perfil(usuario_id: int, respostas: dict):
    """
    Salva ou atualiza o perfil de investidor de um usuário no banco de dados.
    """
    # Primeiro, verificamos se um perfil já existe para este usuário
    perfil_existente = carregar_perfil(usuario_id)
    
    conexao = sqlite3.connect(NOME_BANCO)
    cursor = conexao.cursor()
    try:
        # Extrai os valores do dicionário na ordem correta
        tolerancia = respostas.get("Tolerancia ao risco")
        experiencia = respostas.get("Experiencia")
        liquidez = respostas.get("Necessidade de liquidez")

        if perfil_existente:
            # Se existe, fazemos UPDATE
            print(f"Atualizando perfil para o usuário ID: {usuario_id}")
            cursor.execute("""
                UPDATE perfis 
                SET tolerancia_risco = ?, experiencia = ?, necessidade_liquidez = ?
                WHERE usuario_id = ?
            """, (tolerancia, experiencia, liquidez, usuario_id))
        else:
            # Se não existe, fazemos INSERT
            print(f"Criando novo perfil para o usuário ID: {usuario_id}")
            cursor.execute("""
                INSERT INTO perfis (usuario_id, tolerancia_risco, experiencia, necessidade_liquidez)
                VALUES (?, ?, ?, ?)
            """, (usuario_id, tolerancia, experiencia, liquidez))

        conexao.commit()
    finally:
        conexao.close()

def carregar_perfil(usuario_id: int) -> dict | None:
    """
    Carrega as respostas do perfil de um usuário do banco de dados.
    Retorna um dicionário com as respostas ou None se não houver perfil.
    """
    conexao = sqlite3.connect(NOME_BANCO)
    cursor = conexao.cursor()
    try:
        cursor.execute("""
            SELECT tolerancia_risco, experiencia, necessidade_liquidez 
            FROM perfis 
            WHERE usuario_id = ?
        """, (usuario_id,))
        
        resultado = cursor.fetchone()

        if resultado:
            # 'resultado' é uma tupla, ex: (4, 3, 5)
            # Montamos o dicionário para devolver à aplicação
            respostas = {
                "Tolerancia ao risco": resultado[0],
                "Experiencia": resultado[1],
                "Necessidade de liquidez": resultado[2]
            }
            return respostas
        
        return None
    finally:
        conexao.close()

def atualizar_senha(email: str, nova_senha_hash: str):
    """Atualiza a senha de um usuário existente, identificado pelo e-mail."""
    conexao = sqlite3.connect(NOME_BANCO)
    cursor = conexao.cursor()
    try:
        cursor.execute("UPDATE usuarios SET senha_hash = ? WHERE email = ?", (nova_senha_hash, email))
        conexao.commit()
        print(f"Senha para o usuário {email} foi atualizada no banco de dados.")
    finally:
        conexao.close()

def excluir_perfil(usuario_id: int) -> bool:
    """Exclui o perfil de investidor de um usuário do banco de dados."""
    conexao = sqlite3.connect(NOME_BANCO)
    cursor = conexao.cursor()
    try:
        # O comando DELETE FROM remove as linhas que correspondem à cláusula WHERE
        cursor.execute("DELETE FROM perfis WHERE usuario_id = ?", (usuario_id,))
        conexao.commit()
        
        # A propriedade cursor.rowcount nos diz quantas linhas foram afetadas (deletadas).
        # Se for maior que 0, a exclusão foi bem-sucedida.
        if cursor.rowcount > 0:
            print(f"Perfil do usuário ID {usuario_id} foi excluído do banco de dados.")
            return True
        else:
            print(f"Nenhum perfil encontrado para o usuário ID {usuario_id} para excluir.")
            return False
    finally:
        conexao.close()