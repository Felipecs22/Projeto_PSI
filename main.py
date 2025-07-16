# 1. Importações 
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

    def processar_recuperacao_senha(self):
        """Gerencia o fluxo de recuperação de senha do usuário."""
        limpar_terminal()
        print("--- Recuperação de Conta ---")
        email = input("Digite o e-mail da conta que deseja recuperar: ").strip().lower()

        # 1. Verifica se o usuário realmente existe
        if not self.db.verificar_email_existe(email):
            print("\nE-mail não encontrado no nosso sistema.")
            pausar_e_limpar()
            return

        # 2. Gera e envia o código de recuperação via e-mail
        codigo_recuperacao = random.randint(100000, 999999)
        assunto = "InvestiMatch - Código de Recuperação de Senha"
        conteudo = f"Seu código para redefinir sua senha é: {codigo_recuperacao}"
        
        email_enviado = self.servico_email.enviar_email(email, assunto, conteudo)

        if not email_enviado:
            print("\nFalha ao enviar o e-mail de recuperação. Tente novamente mais tarde.")
            pausar_e_limpar()
            return

        # 3. Pede ao usuário o código recebido e a nova senha
        codigo_digitado = input("Digite o código de recuperação enviado para seu e-mail: ").strip()

        if codigo_digitado == str(codigo_recuperacao):
            print("\nCódigo verificado com sucesso. Agora, crie sua nova senha.")
            nova_senha = input("Digite sua nova senha: ").strip()
            
            # 4. Hasheia a nova senha e manda o banco de dados atualizar
            novo_hash = gerar_hash_senha(nova_senha)
            self.db.atualizar_senha(email, novo_hash)
            
            print("\nSenha redefinida com sucesso!")
        else:
            print("\nCódigo incorreto. A operação foi cancelada por segurança.")

        pausar_e_limpar()
    
    def processar_exclusao_conta(self):
        """Gerencia o fluxo para excluir a conta inteira do usuário logado."""
        limpar_terminal()
        print("--- Excluir Minha Conta ---")
        print("\nATENÇÃO! ESTA AÇÃO É IRREVERSÍVEL! ")
        print("Todos os seus dados, incluindo login, perfil e investimentos registrados, serão apagados permanentemente.")
        
        confirmacao = input("Digite 'excluir' para confirmar a exclusão da sua conta: ").strip()

        if confirmacao.lower() == 'excluir':
            print("\nConfirmado. Excluindo sua conta...")
            
            sucesso = self.db.excluir_conta(self.usuario_logado.id)
            
            if sucesso:
                print("Sua conta foi excluída com sucesso.")
                # Força o logout, já que o usuário não existe mais
                self.usuario_logado = None
            else:
                # Caso raro, mas para segurança
                print("Não foi possível excluir a conta.")
        else:
            print("\nOperação de exclusão cancelada.")

        pausar_e_limpar()
        # A função retornará para o menu_usuario_logado, que verá que o
        # usuario_logado é None e sairá do loop.

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

    def gerenciar_investimentos(self):
        """Mostra o sub-menu para gerenciar os investimentos do usuário."""
        while True:
            limpar_terminal()
            print("--- Meus Investimentos ---")
            print("1 - Registrar novo aporte")
            print("2 - Ver resumo de investimentos")
            print("3 - Ver histórico de aportes")
            print("4 - Voltar ao menu anterior")
            opcao = input("Escolha uma opção: ").strip()

            if opcao == '1':
                self.processar_novo_aporte()
            elif opcao == '2':
                self.visualizar_resumo_investimentos()
            elif opcao == '3':
                self.visualizar_historico_aportes()
            elif opcao == '4':
                break
            else:
                print("\nOpção inválida.")
                pausar_e_limpar()

    def processar_novo_aporte(self):
        """Processa o registro de um novo investimento (aporte)."""
        limpar_terminal()
        print("--- Registrar Novo Aporte ---")
        nome_ativo = input("Digite o nome do ativo específico (ex: Bitcoin, Ação da Petrobras): ").strip()
        nicho = input("Digite o nicho/categoria deste ativo (ex: Cripto, Ações, Renda Fixa): ").strip()
        
        while True:
            try:
                valor_str = input("Digite o valor aportado (ex: 1500.50): R$ ").strip()
                valor_aportado = float(valor_str)
                break
            except ValueError:
                print("Valor inválido. Por favor, use números e ponto para decimais.")
        
        self.db.adicionar_investimento(self.usuario_logado.id, nome_ativo, nicho, valor_aportado)
        pausar_e_limpar()

    def visualizar_resumo_investimentos(self):
        """Busca e exibe o resumo dos investimentos, agrupados por ativo."""
        limpar_terminal()
        print("--- Resumo de Investimentos ---")
        
        resumo = self.db.sumarizar_investimentos_por_ativo(self.usuario_logado.id)
        
        if not resumo:
            print("\nVocê ainda não registrou nenhum investimento.")
        else:
            print(f"\n{'Ativo':<30} {'Nicho (Categoria)':<25} {'Valor Investido (R$)'}")
            print("-" * 75)
            total_geral = 0
            for item in resumo:
                total = item['total_investido']
                total_geral += total
                print(f"{item['nome_ativo']:<30} {item['nicho']:<25} {total:,.2f}")
            
            print("-" * 75)
            print(f"{'VALOR TOTAL GERAL:':<56} {total_geral:,.2f}")
            print("-" * 75)
            
        pausar_e_limpar()

    def visualizar_historico_aportes(self):
        """Busca e exibe o histórico completo de todos os aportes."""
        limpar_terminal()
        print("--- Histórico de Aportes ---")
        
        historico = self.db.carregar_investimentos_do_usuario(self.usuario_logado.id)
        
        if not historico:
            print("\nVocê ainda não registrou nenhum investimento.")
        else:
            print(f"\n{'Data e Hora':<25} {'Ativo':<30} {'Valor (R$)'}")
            print("-" * 75)
            for aporte in historico:
                print(f"{aporte['data_aporte']:<25} {aporte['nome_ativo']:<30} {aporte['valor_aportado']:,.2f}")
            print("-" * 75)
            
        pausar_e_limpar()

    def menu_usuario_logado(self):
        while True:
            limpar_terminal()
            print(f"--- Área do Investidor: {self.usuario_logado.email} ---")
            print("\n1 - Ver/Refazer meu Perfil de Investidor")
            print("2 - Ver Recomendações de Investimento")
            print("3 - Meus Investimentos")
            print("4 - Excluir Minha Conta")
            print("5 - Logout")
            opcao = input("Escolha uma opção: ").strip()

            if opcao == '1':
                self.gerenciar_perfil()
            elif opcao == '2':
                self.exibir_recomendacoes()
            elif opcao == '3':
                self.gerenciar_investimentos()
            elif opcao == '4':
                self.processar_exclusao_conta()
                if not self.usuario_logado:
                    break
            elif opcao == '5':
                print(f"\nFazendo logout de {self.usuario_logado.email}...")
                self.usuario_logado = None
                pausar_e_limpar()
                break
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
            print("3 - Recuperar Conta")
            print("4 - Sair")
            opcao = input("Escolha uma opção: ").strip()

            if opcao == '1':
                self.processar_login()
            elif opcao == '2':                
                self.processar_cadastro()
            elif opcao == '3':
                self.processar_recuperacao_senha()
            elif opcao == '4':
                print("\nEncerrando o sistema... Até logo!")
                break
            else:
                print("\nOpção inválida. Tente novamente.")
                pausar_e_limpar()


# 3. Ponto de Partida da Aplicação
if __name__ == "__main__":
    investimatch = InvestiMatchApp()  
    investimatch.menu_inicial()           