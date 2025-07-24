import database
from models import Usuario, NichoInvestimento, AvaliadorPerfil, Carteira
from utils import limpar_terminal, pausar_e_limpar, gerar_hash_senha
#from services import ServicoEmail
import time
import random


class InvestiMatchApp:
    """A classe principal que orquestra toda a aplicação"""

    def __init__(self):
        """O construtor da classe, executado ao criar o objeto."""
        self.db = database  # guarda uma referência ao nosso módulo de banco de dados
        self.usuario_logado = None  # controla o estado de login
        #self.servico_email = ServicoEmail()

    """ Metodos q chamam as interfaces (alto nível) """

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

            if opcao == "1":
                self.processar_login()
            elif opcao == "2":
                self.processar_cadastro()
            elif opcao == "3":
                self.processar_recuperacao_senha()
            elif opcao == "4":
                print("\nEncerrando o sistema... Até logo!")
                break
            else:
                print("\nOpção inválida. Tente novamente.")
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

            if opcao == "1":
                self.gerenciar_perfil()
            elif opcao == "2":
                self.exibir_recomendacoes()
            elif opcao == "3":
                self.gerenciar_investimentos()
            elif opcao == "4":
                self.processar_exclusao_conta()
                if not self.usuario_logado:
                    break
            elif opcao == "5":
                print(f"\nFazendo logout de {self.usuario_logado.email}...")
                self.usuario_logado = None
                pausar_e_limpar()
                break
            else:
                print("\nOpção inválida.")
                pausar_e_limpar()

    def menu_aportes(self, carteira: object):
        """Mostra o sub-menu para ações dentro de uma carteira específica."""
        while True:
            limpar_terminal()
            print(f"--- Gerenciando a Carteira: '{carteira.nome}' ---")
            print("1 - Registrar novo aporte nesta carteira")
            print("2 - Registrar retirada nesta carteira")
            print("3 - Ver resumo desta carteira")
            print("4 - Ver histórico de aportes desta carteira")
            print("5 - Voltar")
            opcao = input("Escolha uma opção: ").strip()

            if opcao == "1":
                self.processar_novo_aporte(carteira.id)
            elif opcao == "2":
                self.processar_nova_retirada(carteira.id)
            elif opcao == "3":
                self.visualizar_resumo_investimentos(carteira.id)
            elif opcao == "4":
                self.visualizar_historico_aportes(carteira.id)
            elif opcao == "5":
                break
            else:
                print("\nOpção inválida.")
                pausar_e_limpar()

    def gerenciar_investimentos(self):
        """Método principal que lista carteiras e direciona para criação ou gerenciamento."""

        while True:
            limpar_terminal()
            print("--- Gerenciador de Investimentos ---")

            # Busca todas as carteiras do usuário logado
            carteiras = self.db.listar_carteiras_do_usuario(self.usuario_logado.id)

            if not carteiras:
                print(
                    "\nVocê ainda não tem nenhuma carteira de investimentos. Selecione a opção '1' para criar sua primeira!"
                )
            else:
                print("\nSuas carteiras:")
                for carteira in carteiras:
                    print(f"  - {carteira.nome} (ID: {carteira.id})")

            print("\nOpções:")
            print("1 - Criar nova carteira")
            print("2 - Gerenciar uma carteira existente")
            print("3 - Excluir uma carteira")
            print("4 - Voltar")
            opcao = input("Escolha uma opção: ").strip()

            if opcao == "1":
                self.processar_nova_carteira()
            elif opcao == "2":
                if not carteiras:
                    print("\nVocê precisa criar uma carteira primeiro.")
                    pausar_e_limpar()
                else:
                    self.selecionar_carteira(carteiras)
            elif opcao == "3":
                if not carteiras:
                    print("\nNão há carteiras para excluir.")
                    pausar_e_limpar()
                else:
                    self.processar_exclusao_carteira(carteiras)
            elif opcao == "4":
                break
            else:
                print("Opção inválida.")
                pausar_e_limpar()

    def exibir_recomendacoes(self):
        """Carrega o perfil, gera e exibe recomendações detalhadas com pausas e destaques."""
        limpar_terminal()
        print("--- Analisando seu perfil para gerar as melhores recomendações... ---")
        time.sleep(2)  # Pequena pausa inicial
        limpar_terminal()
        print("--- Recomendações de Investimento Personalizadas ---")

        perfil = self.db.carregar_perfil(self.usuario_logado.id)
        if not perfil:
            print(
                "\nVocê precisa preencher seu Perfil de Investidor primeiro (Opção 1 no menu)."
            )
            pausar_e_limpar()
            return

        nichos_disponiveis = [
            NichoInvestimento(
                nome="Renda Fixa",
                risco=1,
                experiencia=1,
                liquidez=5,
                descricao="Ativos com baixo risco e retorno mais previsível, ideais para segurança e para iniciantes.",
                exemplos="Exemplos: Tesouro Selic, CDBs de grandes bancos, LCI/LCA.",
            ),
            NichoInvestimento(
                nome="Fundos Imobiliários (FIIs)",
                risco=3,
                experiencia=3,
                liquidez=3,
                descricao="Permitem investir no setor imobiliário e receber aluguéis mensais com risco moderado.",
                exemplos="Exemplos: Fundos de Tijolo (shoppings, galpões) e Papel (dívidas imobiliárias).",
            ),
            NichoInvestimento(
                nome="Ações Brasileiras",
                risco=4,
                experiencia=4,
                liquidez=3,
                descricao="Frações de grandes empresas. Potencial de alto retorno no longo prazo, com maior risco.",
                exemplos="Exemplos: Ações de empresas como Petrobras, Vale, Itaú.",
            ),
            NichoInvestimento(
                nome="Criptomoedas",
                risco=5,
                experiencia=4,
                liquidez=4,
                descricao="Ativos digitais descentralizados, com altíssimo risco e potencial de valorização expressiva.",
                exemplos="Exemplos: Bitcoin (BTC), Ethereum (ETH).",
            ),
        ]

        avaliador = AvaliadorPerfil(perfil)
        ranking = avaliador.gerar_ranking(nichos_disponiveis)

        soma_das_pontuacoes = sum(
            item["pontuacao"] for item in ranking if item["pontuacao"] > 0
        )

        # 1. PONTUAÇÃO MÁXIMA: Definimos o valor máximo possível para a pontuação.
        PONTUACAO_MAXIMA = 15

        print(
            "\nBaseado no seu perfil, aqui está uma sugestão de como alocar seus próximos investimentos:"
        )
        print("-" * 80)
        time.sleep(1)

        for item_ranking in ranking:
            pontuacao = item_ranking["pontuacao"]
            if pontuacao <= 0:
                continue

            percentual = (
                (pontuacao / soma_das_pontuacoes) * 100
                if soma_das_pontuacoes > 0
                else 0
            )
            nicho_obj = next(
                (n for n in nichos_disponiveis if n.nome == item_ranking["nicho"]), None
            )

            print(f"▶ {item_ranking['nicho']} | Alocação Sugerida: {percentual:.2f}%")

            # 2. NOVA EXIBIÇÃO: Adicionamos a pontuação e a mensagem "DEU MATCH!"
            print(f"  Compatibilidade: {pontuacao}/{PONTUACAO_MAXIMA} pontos")
            if pontuacao > 12:
                print(
                    "  ✨ DEU MATCH! ✨ Este nicho é altamente compatível com seu perfil!"
                )

            if nicho_obj:
                print(f"  Descrição: {nicho_obj.descricao}")
                print(f"  {nicho_obj.exemplos}")

            print("-" * 80)

            # 3. PAUSA: Adicionamos um ritmo à apresentação.
            time.sleep(2.5)  # Pausa de 2.5 segundos entre cada recomendação

        pausar_e_limpar()

    def visualizar_historico_aportes(self, carteira_id: int):
        """Busca e exibe o histórico completo de aportes de uma carteira específica."""
        limpar_terminal()
        print("--- Histórico de Aportes da Carteira ---")

        # A chamada agora usa a nova função nomeada e corrigida
        historico = self.db.carregar_historico_carteira(carteira_id)

        if not historico:
            print(
                "\nNenhum investimento registrado nesta carteira. No menu anterior, selecione a opção '1' para registrar seu primeiro investimento!"
            )
        else:
            # Ajustamos a tabela para mostrar o nicho também
            print(f"\n{'Data e Hora':<25} {'Ativo':<30} {'Nicho':<20} {'Valor (R$)'}")
            print("-" * 95)
            for aporte in historico:
                print(
                    f"{aporte['data_aporte']:<25} {aporte['nome_ativo']:<30} {aporte['nicho']:<20} {aporte['valor_aportado']:,.2f}"
                )
            print("-" * 95)

        pausar_e_limpar()

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

            if input("\nDeseja refazer o questionário? (s/n): ").strip().lower() != "s":
                pausar_e_limpar()
                return  # Volta ao menu logado
        else:
            print("\nVocê ainda não preencheu seu perfil de investidor.")
            input("Pressione Enter para começar o questionário...")

        # 2. Pede as novas respostas
        novas_respostas = self.pedir_respostas()

        # 3. Salva as novas respostas no banco de dados
        self.db.salvar_ou_atualizar_perfil(self.usuario_logado.id, novas_respostas)

        print("\nPerfil salvo/atualizado com sucesso!")
        pausar_e_limpar()

    """ Metodos de processamento """

    def processar_cadastro(self):
        limpar_terminal()
        print("--- Cadastro de Novo Usuário ---")
        email = input("Digite seu email: ").strip().lower()

        if self.db.email_existe(email):
            print("\nEste email já está cadastrado.")
            pausar_e_limpar()
            return

        senha = self.validar_senha("Crie sua nova senha")
        #comentado para correção de bug
        ''' codigo_verificacao = random.randint(100000, 999999)
        assunto = "InvestiMatch - Código de Verificação"
        conteudo = f"Seu código de verificação para o cadastro é: {codigo_verificacao}"

        email_enviado = self.servico_email.enviar_email(email, assunto, conteudo)

        if not email_enviado:
            print("\nNão foi possível validar seu e-mail. O cadastro foi cancelado.")
            pausar_e_limpar()
            return

        codigo_digitado = input(
            "Digite o código de verificação enviado para o seu e-mail: "
        ).strip()

        if codigo_digitado != str(codigo_verificacao):
            print("\nCódigo de verificação incorreto. O cadastro foi cancelado.")
            pausar_e_limpar()
            return

        print("\nE-mail verificado com sucesso!")'''
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

        usuario_encontrado = self.db.buscar_usuario(email)

        hash_digitado = gerar_hash_senha(senha)

        if usuario_encontrado and usuario_encontrado.senha == hash_digitado:
            self.usuario_logado = usuario_encontrado
            self.menu_usuario_logado()
        else:
            print("\nEmail ou senha inválidos.")
            pausar_e_limpar()

    '''def processar_recuperacao_senha(self):
        """Gerencia o fluxo de recuperação de senha do usuário."""
        limpar_terminal()
        print("--- Recuperação de Conta ---")
        email = input("Digite o e-mail da conta que deseja recuperar: ").strip().lower()

        # Verifica se o usuário realmente existe
        if not self.db.email_existe(email):
            print("\nE-mail não encontrado no nosso sistema.")
            pausar_e_limpar()
            return

        # gera e envia o código de recuperação
        codigo_recuperacao = random.randint(100000, 999999)
        assunto = "InvestiMatch - Código de Recuperação de Senha"
        conteudo = f"Seu código para redefinir sua senha é: {codigo_recuperacao}"

        email_enviado = self.servico_email.enviar_email(email, assunto, conteudo)

        if not email_enviado:
            print(
                "\nFalha ao enviar o e-mail de recuperação. Tente novamente mais tarde."
            )
            pausar_e_limpar()
            return

        codigo_digitado = input(
            "Digite o código de recuperação enviado para seu e-mail: "
        ).strip()

        if codigo_digitado == str(codigo_recuperacao):
            print("\nCódigo verificado com sucesso. Agora, crie sua nova senha.")
            requisitos = (
                "(Mínimo 8 caracteres, com letras maiúsculas, minúsculas e números)"
            )
            nova_senha = self._pedir_e_validar_senha("Digite sua nova senha")

            # hasheia a nova senha e mando o banco de dados atualizar
            novo_hash = gerar_hash_senha(nova_senha)
            self.db.atualizar_senha(email, novo_hash)

            print("\nSenha redefinida com sucesso!")
        else:
            print("\nCódigo incorreto. A operação foi cancelada por segurança.")

        pausar_e_limpar()'''

    def processar_exclusao_conta(self):
        """Gerencia o fluxo para excluir a conta inteira do usuário logado."""
        limpar_terminal()
        print("--- Excluir Minha Conta ---")
        print("\nATENÇÃO! ESTA AÇÃO É IRREVERSÍVEL! ")
        print(
            "Todos os seus dados, incluindo login, perfil e investimentos registrados, serão apagados permanentemente."
        )

        confirmacao = input(
            "Digite 'excluir' para confirmar a exclusão da sua conta: "
        ).strip()

        if confirmacao.lower() == "excluir":
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

    def pedir_respostas(self) -> dict:
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
            "Necessidade de liquidez": "Qual sua necessidade de ter o dinheiro disponível para resgate (1: Muito alta - 5: Muito baixa)? ",
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

    def processar_nova_carteira(self):
        """Processa a criação de uma nova carteira com validação de input."""
        limpar_terminal()
        print("--- Criar Nova Carteira ---")

        while True:
            nome_carteira = input(
                "Digite o nome para a nova carteira (ex: Aposentadoria): "
            ).strip()
            if nome_carteira:  # Se o nome não for uma string vazia
                break  # Sai do loop, pois o nome é válido
            else:
                print("ERRO: O nome da carteira não pode ser vazio. Tente novamente.")

        # O código só continua daqui quando um nome válido for inserido
        nova_carteira = Carteira(nome=nome_carteira, usuario_id=self.usuario_logado.id)
        self.db.criar_carteira(nova_carteira)
        pausar_e_limpar()

    def selecionar_carteira(self, carteiras):
        """Pede ao usuário para escolher uma carteira e entra no menu de aportes."""
        while True:
            try:
                id_selecionado = int(
                    input("\nDigite o ID da carteira que deseja gerenciar: ").strip()
                )
                # Procura a carteira selecionada na lista que já temos
                carteira_selecionada = next(
                    (c for c in carteiras if c.id == id_selecionado), None
                )

                if carteira_selecionada:
                    # Se encontrou, entramos no sub-menu de aportes
                    self.menu_aportes(carteira_selecionada)
                    break  # Sai deste loop de seleção
                else:
                    print("ID de carteira inválido.")
            except ValueError:
                print("Por favor, digite um número válido.")

    def processar_novo_aporte(self, carteira_id: int):
        """Processa o registro de um novo aporte com validação de inputs."""
        limpar_terminal()
        print("--- Registrar Novo Aporte ---")

        while True:
            nome_ativo = input(
                "Digite o nome do ativo específico (ex: Bitcoin, Ação da Petrobras): "
            ).strip()
            if nome_ativo:
                break
            print("ERRO: O nome do ativo não pode ser vazio.")

        while True:
            nicho = input(
                "Digite o nicho/categoria deste ativo (ex: Cripto, Ações, Renda Fixa): "
            ).strip()
            if nicho:
                break
            print("ERRO: O nicho não pode ser vazio.")

        while True:
            try:
                valor_str = input("Digite o valor aportado (ex: 1500.50): R$ ").strip()
                valor_aportado = float(valor_str)
                if valor_aportado > 0:
                    break
                else:
                    print("ERRO: O valor deve ser positivo.")
            except ValueError:
                print(
                    "ERRO: Valor inválido. Por favor, use números e ponto para decimais."
                )

        self.db.adicionar_investimento(carteira_id, nome_ativo, nicho, valor_aportado)
        pausar_e_limpar()

    def processar_nova_retirada(self, carteira_id: int):
        """Processa o registro de uma retirada, mostrando o resumo e inferindo o nicho."""
        limpar_terminal()
        print("--- Registrar Nova Retirada ---")

        # 1. Mostra o resumo para dar contexto ao usuário
        print("Este é o resumo atual da sua carteira:")
        resumo_atual = self.db.sumarizar_investimentos(carteira_id)
        self._exibir_tabela_resumo(resumo_atual)

        if not resumo_atual:
            pausar_e_limpar()
            return

        # 2. Pede o nome do ativo e valida se ele existe
        while True:
            nome_ativo = input(
                "\nDe qual ativo você retirou o valor (digite o nome exato)? "
            ).strip()
            if not nome_ativo:
                print("ERRO: O nome não pode ser vazio.")
                continue

            # 3. Busca o nicho automaticamente!
            nicho_encontrado = self.db.buscar_nicho(carteira_id, nome_ativo)

            if nicho_encontrado:
                print(f"-> Ativo encontrado no nicho: '{nicho_encontrado}'")
                break
            else:
                print(
                    f"ERRO: Ativo '{nome_ativo}' não encontrado nesta carteira. Verifique o nome e tente novamente."
                )

        # 4. Pede o valor a ser retirado
        while True:
            try:
                valor_str = input("Digite o valor retirado (ex: 250.00): R$ ").strip()
                valor_retirado = float(valor_str)
                if valor_retirado > 0:
                    break
                else:
                    print("ERRO: O valor deve ser positivo.")
            except ValueError:
                print("ERRO: Valor inválido.")

        # 5. Registra o investimento com valor negativo
        valor_negativo = -abs(valor_retirado)
        self.db.adicionar_investimento(
            carteira_id, nome_ativo, nicho_encontrado, valor_negativo
        )
        pausar_e_limpar()

    def visualizar_resumo_investimentos(self, carteira_id: int):
        """Busca e exibe o resumo dos investimentos de uma carteira específica."""
        limpar_terminal()
        print("--- Resumo de Investimentos da Carteira ---")

        resumo = self.db.sumarizar_investimentos(carteira_id)
        self._exibir_tabela_resumo(resumo)  # Reutilizando nosso novo método!

        pausar_e_limpar()

    def processar_exclusao_carteira(self, carteiras: list):
        """Processa a exclusão de uma carteira existente."""
        try:
            id_para_excluir = int(
                input("\nDigite o ID da carteira que deseja EXCLUIR: ").strip()
            )
            # Verifica se o ID fornecido corresponde a uma das carteiras do usuário
            carteira_existe = any(c.id == id_para_excluir for c in carteiras)

            if not carteira_existe:
                print("\nID inválido ou não pertence a você.")
                pausar_e_limpar()
                return

            print(
                f"\n🛑 ATENÇÃO: Você está prestes a excluir a carteira com ID {id_para_excluir}."
            )
            print("Todos os investimentos registrados nela serão perdidos para sempre.")
            confirmacao = input("Digite 'excluir' para confirmar: ").strip().lower()

            if confirmacao == "excluir":
                self.db.excluir_carteira(id_para_excluir)
            else:
                print("\nExclusão cancelada.")

            pausar_e_limpar()

        except ValueError:
            print("\nEntrada inválida. Por favor, digite um número de ID.")
            pausar_e_limpar()

    """metodos auxiliares"""

    def validar_senha(self, prompt: str) -> str:
        """
        Pede uma senha válida ao usuário
        """
        requisitos = "(Mínimo 8 caracteres, com maiúsculas, minúsculas e números)"
        print(f"\n{prompt}: {requisitos}")

        while True:
            senha = input("Digite a senha: ").strip()

            if len(senha) < 8:
                print("ERRO: A senha deve ter pelo menos 8 caracteres.")
                continue
            if not any(c.isupper() for c in senha):
                print("ERRO: A senha deve conter pelo menos uma letra maiúscula.")
                continue
            if not any(c.islower() for c in senha):
                print("ERRO: A senha deve conter pelo menos uma letra minúscula.")
                continue
            if not any(c.isdigit() for c in senha):
                print("ERRO: A senha deve conter pelo menos um número.")
                continue

            senha_confirmada = input("Confirme a senha: ").strip()
            if senha == senha_confirmada:
                return senha
            else:
                print("ERRO: As senhas não coincidem. Tente novamente.")

    def _exibir_tabela_resumo(self, resumo_dados: list):
        """Método interno que recebe dados de resumo e os exibe em formato de tabela."""
        if not resumo_dados:
            print("\nNenhum investimento registrado nesta carteira.")
            return

        print(f"\n{'Ativo':<30} {'Nicho (Categoria)':<25} {'Valor Investido (R$)'}")
        print("-" * 75)
        total_geral = 0
        for item in resumo_dados:
            total = item["total_investido"]
            total_geral += total
            print(f"{item['nome_ativo']:<30} {item['nicho']:<25} {total:,.2f}")

        print("-" * 75)
        print(f"{'VALOR TOTAL GERAL:':<56} {total_geral:,.2f}")
        print("-" * 75)


# Ponto de partida
if __name__ == "__main__":
    investimatch = InvestiMatchApp()
    investimatch.menu_inicial()
