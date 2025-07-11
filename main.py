# Em main.py (Versão Final OOP)

# 1. Importações dos nossos módulos e de bibliotecas
import database
from models import Usuario
from utils import limpar_terminal, pausar_e_limpar
import time

# 2. Definição da classe principal da aplicação
class InvestiMatchApp:
    """A classe principal que orquestra toda a aplicação."""

    def __init__(self):
        """O construtor da classe, executado ao criar o objeto."""
        self.db = database  # Guarda uma referência ao nosso módulo de banco de dados
        self.usuario_logado = None  # Controla o estado de login

    def processar_cadastro(self):
        """Processa o fluxo de cadastro de um novo usuário."""
        limpar_terminal()
        print("--- Cadastro de Novo Usuário ---")
        email = input("Digite seu email: ").strip().lower()

        if self.db.verificar_email_existe(email):
            print("\nEste email já está cadastrado.")
            pausar_e_limpar()
            return

        senha = input("Crie sua senha: ").strip()
        
        try:
            novo_usuario = Usuario(email=email, senha=senha)
            self.db.adicionar_usuario(novo_usuario)
            print("\nCadastro realizado com sucesso!")
        except ValueError as e:
            print(f"\nErro no cadastro: {e}")
        
        pausar_e_limpar()

    def processar_login(self):
        """Processa o fluxo de login de um usuário."""
        limpar_terminal()
        print("--- Login ---")
        email = input("Email: ").strip().lower()
        senha = input("Senha: ").strip()

        usuario_encontrado = self.db.buscar_usuario_por_email(email)
        
        if usuario_encontrado and usuario_encontrado.senha == senha:
            self.usuario_logado = usuario_encontrado
            self.menu_usuario_logado()
        else:
            print("\nEmail ou senha inválidos.")
            pausar_e_limpar()
    
    def menu_usuario_logado(self):
        """Mostra o menu de opções para um usuário que está logado."""
        limpar_terminal()
        
        while True:
            print(f"--- Área do Investidor: {self.usuario_logado.email} ---")
            print("\n1 - Ver/Refazer meu Perfil de Investidor")
            print("2 - Ver Recomendações de Investimento")
            print("3 - Logout")
            opcao = input("Escolha uma opção: ").strip()

            if opcao == '1':
                print("\nFuncionalidade de Perfil ainda não implementada.")
                pausar_e_limpar()
            elif opcao == '2':
                print("\nFuncionalidade de Recomendações ainda não implementada.")
                pausar_e_limpar()
            elif opcao == '3':
                # Implementando o Logout
                print(f"\nFazendo logout de {self.usuario_logado.email}...")
                self.usuario_logado = None # Limpa o estado do usuário logado
                pausar_e_limpar()
                break # Quebra o loop do menu logado, retornando ao menu principal
            else:
                print("\nOpção inválida.")
                pausar_e_limpar()

    def executar(self):
        """Inicia a execução principal do programa e mostra o menu de autenticação."""
        self.db.inicializar_db()

        while True:
            limpar_terminal()
            print("--- Bem-vindo ao InvestiMatch! ---")
            print("1 - Fazer Login")
            print("2 - Cadastrar-se")
            print("3 - Sair")
            opcao = input("Escolha uma opção: ").strip()

            if opcao == '1':
                self.processar_login()
            elif opcao == '2':
                self.processar_cadastro()
            elif opcao == '3':
                print("\nEncerrando o sistema... Até logo!")
                break
            else:
                print("\nOpção inválida. Tente novamente.")
                pausar_e_limpar()


# 3. Ponto de Partida da Aplicação
if __name__ == "__main__":
    investimatch = InvestiMatchApp()  # Cria uma instância da nossa aplicação
    investimatch.executar()           # Roda o método principal