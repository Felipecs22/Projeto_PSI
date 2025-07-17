import datetime
import sqlite3
from models import Usuario, Carteira
NOME_BANCO = "investimatch.db"

def inicializar_db():
    """
    Cria as tabelas do banco de dados com a NOVA estrutura de carteiras.
    """
    print("Inicializando banco de dados com nova estrutura...")
    
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

        # Tabela de perfis 
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS perfis (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER NOT NULL,
            tolerancia_risco INTEGER,
            experiencia INTEGER,
            necessidade_liquidez INTEGER,
            FOREIGN KEY (usuario_id) REFERENCES usuarios (id) ON DELETE CASCADE
        )
        """)

        # TABELA para as carteiras (portfólios) do usuário
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS carteiras (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER NOT NULL,
            nome TEXT NOT NULL,
            FOREIGN KEY (usuario_id) REFERENCES usuarios (id) ON DELETE CASCADE
        )
        """)
        
        # 2. TABELA de investimentos
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS investimentos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            carteira_id INTEGER NOT NULL, -- MUDANÇA: agora se conecta à carteira
            nome_ativo TEXT NOT NULL,
            nicho TEXT NOT NULL,
            valor_aportado REAL NOT NULL,
            data_aporte TEXT NOT NULL,
            FOREIGN KEY (carteira_id) REFERENCES carteiras (id) ON DELETE CASCADE
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

def excluir_conta(usuario_id: int) -> bool:
    """
    Exclui todos os dados de um usuário (perfil, investimentos e a própria conta)
    do banco de dados.
    """
    conexao = sqlite3.connect(NOME_BANCO)
    cursor = conexao.cursor()
    try:
        # É crucial executar as exclusões nesta ordem
        
        # 1. Deleta o perfil do investidor
        cursor.execute("DELETE FROM perfis WHERE usuario_id = ?", (usuario_id,))
        
        # 2. Deleta os investimentos registrados
        cursor.execute("DELETE FROM investimentos WHERE usuario_id = ?", (usuario_id,))
        
        # 3. Por último, deleta o usuário
        cursor.execute("DELETE FROM usuarios WHERE id = ?", (usuario_id,))
        
        conexao.commit()
        
        if cursor.rowcount > 0:
            print(f"Conta completa do usuário ID {usuario_id} foi excluída do banco.")
            return True
        else:
            # Isso não deveria acontecer se a função for chamada para um usuário logado
            print(f"Nenhuma conta encontrada para o usuário ID {usuario_id}.")
            return False
            
    finally:
        conexao.close()

def criar_carteira(carteira: object) -> int:
    """
    Salva um novo objeto Carteira no banco de dados.
    Retorna o ID da carteira recém-criada.
    """
    conexao = sqlite3.connect(NOME_BANCO)
    cursor = conexao.cursor()
    try:
        cursor.execute(
            "INSERT INTO carteiras (usuario_id, nome) VALUES (?, ?)",
            (carteira.usuario_id, carteira.nome)
        )
        conexao.commit()
        # cursor.lastrowid retorna o ID da última linha inserida
        id_criado = cursor.lastrowid
        print(f"Carteira '{carteira.nome}' criada com sucesso com o ID: {id_criado}.")
        return id_criado
    finally:
        conexao.close()

def listar_carteiras_do_usuario(usuario_id: int) -> list:
    """Busca e retorna uma lista de objetos Carteira para um usuário específico."""
    conexao = sqlite3.connect(NOME_BANCO)
    cursor = conexao.cursor()
    try:
        cursor.execute("SELECT id, nome, usuario_id FROM carteiras WHERE usuario_id = ?", (usuario_id,))
        # fetchall() busca todos os resultados que correspondem à consulta
        resultados_brutos = cursor.fetchall()
        
        # Transforma os resultados brutos (tuplas) em uma lista de objetos Carteira
        lista_de_carteiras = []
        for row in resultados_brutos:
            # row[0] é o id, row[1] é o nome, row[2] é o usuario_id
            carteira = Carteira(id=row[0], nome=row[1], usuario_id=row[2])
            lista_de_carteiras.append(carteira)
            
        return lista_de_carteiras
    finally:
        conexao.close()

def adicionar_investimento(carteira_id: int, nome_ativo: str, nicho: str, valor_aportado: float):
    """Salva um novo registro de investimento no banco de dados para uma carteira específica."""
    conexao = sqlite3.connect(NOME_BANCO)
    cursor = conexao.cursor()
    try:
        data_atual = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # A ordem das variáveis na tupla deve ser a mesma da instrução INSERT
        cursor.execute("""
            INSERT INTO investimentos (carteira_id, nome_ativo, nicho, valor_aportado, data_aporte)
            VALUES (?, ?, ?, ?, ?)
        """, (carteira_id, nome_ativo, nicho, valor_aportado, data_atual))
        
        conexao.commit()
        print(f"Investimento em {nome_ativo} de R$ {valor_aportado:.2f} registrado com sucesso.")
    finally:
        conexao.close()

def sumarizar_investimentos_por_ativo(carteira_id: int) -> list:
    """Carrega os investimentos de UMA CARTEIRA, agrupando por ativo e somando os valores."""
    conexao = sqlite3.connect(NOME_BANCO)
    conexao.row_factory = sqlite3.Row
    cursor = conexao.cursor()
    try:
        # A mudança principal é no WHERE, para filtrar pela carteira correta
        cursor.execute("""
            SELECT nome_ativo, nicho, SUM(valor_aportado) as total_investido
            FROM investimentos
            WHERE carteira_id = ?
            GROUP BY nome_ativo, nicho
            ORDER BY total_investido DESC
        """, (carteira_id,))
        
        resultados = cursor.fetchall()
        return [dict(row) for row in resultados]
    finally:
        conexao.close()

def carregar_historico_da_carteira(carteira_id: int) -> list:
    """Carrega o histórico completo de aportes de uma carteira específica."""
    conexao = sqlite3.connect(NOME_BANCO)
    conexao.row_factory = sqlite3.Row 
    cursor = conexao.cursor()
    try:
        # A mudança crucial é no WHERE, e adicionamos uma ordenação por data
        cursor.execute("""
            SELECT nome_ativo, nicho, valor_aportado, data_aporte 
            FROM investimentos 
            WHERE carteira_id = ? 
            ORDER BY data_aporte DESC
        """, (carteira_id,))
        
        resultados = cursor.fetchall() 
        return [dict(row) for row in resultados]
    finally:
        conexao.close()
