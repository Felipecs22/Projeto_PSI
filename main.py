# 1. Importações dos nossos módulos e de bibliotecas
import database
from models import Usuario, NichoInvestimento, AvaliadorPerfil
from utils import limpar_terminal, pausar_e_limpar, gerar_hash_senha
from services import ServicoEmail
import time
import random

# 2. Definição da classe principal da aplicação
class InvestiMatchApp:
    """A classe principal que orquestra toda a aplicação."""

    def __init__(self):
        """O construtor da classe, executado ao criar o objeto."""
        self.db = database  # Guarda uma referência ao nosso módulo de banco de dados
        self.usuario_logado = None  # Controla o estado de login
        self.servico_email = ServicoEmail()

    def processar_cadastro(self):
        limpar_terminal()
        print("--- Cadastro de Novo Usuário ---")
        email = input("Digite seu email: ").strip().lower()

        if self.db.verificar_email_existe(email):
            print("\nEste email já está cadastrado.")
            pausar_e_limpar()
            return

        senha = input("Crie sua senha: ").strip()

        codigo_verificacao = random.randint(100000, 999999)
        assunto = "InvestiMatch - Código de Verificação"
        conteudo = f"Seu código de verificação para o cadastro é: {codigo_verificacao}"

        email_enviado = self.servico_email.enviar_email(email, assunto, conteudo)

        if not email_enviado:
            print("\nNão foi possível validar seu e-mail. O cadastro foi cancelado.")
            pausar_e_limpar()
            return

        codigo_digitado = input("Digite o código de verificação enviado para o seu e-mail: ").strip()

        if codigo_digitado != str(codigo_verificacao):
            print("\nCódigo de verificação incorreto. O cadastro foi cancelado.")
            pausar_e_limpar()
            return

        print("\nE-mail verificado com sucesso!")
        try:
            hash_da_senha = gerar_hash_senha(senha)
            novo_usuario = Usuario(email=email, senha=hash_da_senha)
            self.db.adicionar_usuario(novo_usuario)
            print("Cadastro finalizado com sucesso!")
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
        
        hash_digitado = gerar_hash_senha(senha)

        if usuario_encontrado and usuario_encontrado.senha == hash_digitado:
            self.usuario_logado = usuario_encontrado
            self.menu_usuario_logado()
        else:
            print("\nEmail ou senha inválidos.")
            pausar_e_limpar()

    def _pedir_respostas_investidor(self) -> dict:
        """
        Método auxiliar para fazer o questionário ao usuário e validar as respostas.
        O _ no início do nome sugere que é um método 'interno' da classe.
        """
        limpar_terminal()
        print("--- Questionário de Perfil de Investidor ---")
        print("\nResponda com um número de 1 a 5 para cada pergunta.")
        
        perguntas = {
            "Tolerancia ao risco": "Qual sua disposição a correr riscos (1: Nenhuma - 5: Total)? ",
            "Experiencia": "Qual seu nível de experiência com investimentos (1: Nenhuma - 5: Muita)? ",
            "Necessidade de liquidez": "Qual sua necessidade de ter o dinheiro disponível para resgate (1: Muito alta - 5: Muito baixa)? "
        }
        
        respostas = {}
        for chave, texto_pergunta in perguntas.items():
            while True:
                try:
                    resposta_num = int(input(f"\n{texto_pergunta}").strip())
                    if 1 <= resposta_num <= 5:
                        respostas[chave] = resposta_num
                        break
                    else:
                        print("Por favor, digite um número entre 1 e 5.")
                except ValueError:
                    print("Entrada inválida. Por favor, digite um número.")
        return respostas

    def gerenciar_perfil(self):
        """Orquestra a visualização e atualização do perfil do investidor."""
        limpar_terminal()
        print("--- Meu Perfil de Investidor ---")
        
        # 1. Carrega o perfil existente do banco de dados
        perfil_atual = self.db.carregar_perfil(self.usuario_logado.id)

        if perfil_atual:
            print("\nSeu perfil atual é:")
            for chave, valor in perfil_atual.items():
                print(f"  - {chave}: {valor}")
            
            if input("\nDeseja refazer o questionário? (s/n): ").strip().lower() != 's':
                pausar_e_limpar()
                return # Volta ao menu logado
        else:
            print("\nVocê ainda não preencheu seu perfil de investidor.")
            input("Pressione Enter para começar o questionário...")

        # 2. Pede as novas respostas
        novas_respostas = self._pedir_respostas_investidor()
        
        # 3. Salva as novas respostas no banco de dados
        self.db.salvar_ou_atualizar_perfil(self.usuario_logado.id, novas_respostas)
        
        print("\nPerfil salvo/atualizado com sucesso!")
        pausar_e_limpar()

    def exibir_recomendacoes(self):
        """Carrega o perfil do usuário, gera e exibe as recomendações de investimento."""
        limpar_terminal()
        print("--- Recomendações de Investimento ---")

        # 1. Carrega o perfil do usuário
        perfil = self.db.carregar_perfil(self.usuario_logado.id)

        if not perfil:
            print("\nVocê precisa preencher seu Perfil de Investidor primeiro.")
            print("Selecione a opção 1 no menu.")
            pausar_e_limpar()
            return

        # 2. Prepara os dados para o avaliador
        nichos_disponiveis = [
            NichoInvestimento(nome="Tesouro Selic (Renda Fixa)", risco=1, experiencia=1, liquidez=5),
            NichoInvestimento(nome="CDBs (Liquidez Diária)", risco=2, experiencia=2, liquidez=4),
            NichoInvestimento(nome="Fundos Imobiliários (FIIs)", risco=3, experiencia=3, liquidez=3),
            NichoInvestimento(nome="Ações Brasileiras", risco=4, experiencia=4, liquidez=3),
            NichoInvestimento(nome="Criptomoedas", risco=5, experiencia=4, liquidez=4)
        ]

        # 3. Usa o 'cérebro' para obter o ranking
        avaliador = AvaliadorPerfil(perfil)
        ranking = avaliador.gerar_ranking(nichos_disponiveis)
        
        # 4. Exibe o resultado
        print("\nBaseado no seu perfil, este é o ranking de adequação para cada nicho:")
        for i, item in enumerate(ranking):
            print(f"  {i+1}º - {item['nicho']} (Pontuação de Compatibilidade: {item['pontuacao']})")
        
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
                self.gerenciar_perfil()
            elif opcao == '2':
                self.exibir_recomendacoes()
            elif opcao == '3':
                # Implementando o Logout
                print(f"\nFazendo logout de {self.usuario_logado.email}...")
                self.usuario_logado = None # Limpa o estado do usuário logado
                pausar_e_limpar()
                break # Quebra o loop do menu logado, retornando ao menu principal
            else:
                print("\nOpção inválida.")
                pausar_e_limpar()
    
    def menu_inicial(self):
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
    investimatch.menu_inicial()           # Roda o método principal