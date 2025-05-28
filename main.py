import re
import random
import time
import smtplib
from email.message import EmailMessage
import os

#configurações 
ARQUIVO_PERFIS = "perfis_investidores.txt"
EMAIL_REMETENTE = "fcsantos2201@gmail.com"  #email que vai interagir com user
SENHA_APP = "zvwjliixtnnwkirm"  #senha app gmail
ARQUIVO_USUARIOS = "usuarios.txt" #arquivo email+senha
PROFILE_KEYS_ORDER = ["Tolerancia ao risco", "Experiencia", "Necessidade de liquidez"] #ordenando dicionario perfil


#Funções gerais

#Envia um e-mail com código de segurança
def enviar_email(destinatario, codigo, info_mensagem):
    msg = EmailMessage()
    msg["Subject"] = "Sistema de Autenticação - Código de segurança"
    msg["From"] = EMAIL_REMETENTE
    msg["To"] = destinatario
    msg.set_content(f"{info_mensagem} {codigo}")

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(EMAIL_REMETENTE, SENHA_APP)
            smtp.send_message(msg)
        print(" Código de verificação enviado para o seu email!")
    except Exception as e:
        print(f" Erro ao enviar email: {e}")
       
#limpa o console
def limpar_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

#aguarda um enter e limpa o console
def pausar_e_limpar():
    input("\nPressione Enter para continuar...")
    limpar_terminal()


#Validações de autenticação

#pede e valida o formato do e-mail inserido
def validar_email():
    while True:
        email = input("Digite seu email (Ex: usuario@dominio.com): ").strip().lower()
        if re.fullmatch(r"[^@]+@[^@]+\.[^@]+", email):
            return email
        print("Email inválido! Verifique o formato (deve conter '@' e '.')")

#valida a criação de senha e confirma com código enviado por e-mail
def validar_senha(email_destinatario):
    while True:
        senha = input("Crie sua nova senha (8 caracteres, letras, números, 1 maiúscula. Ex: Senha123): ").strip()

        if not senha.isalnum():
            print("Senha inválida. Use apenas letras e números")
            continue
        
        if not (len(senha) == 8 and re.search(r"[A-Z]", senha) and re.search(r"[a-z]", senha) and re.search(r"[0-9]", senha)):
            print("Senha inválida. Deve ter 8 caracteres, maiúscula, minúscula e número")
            continue

        confirmar_senha = input("Confirme sua senha: ").strip()
        if confirmar_senha == senha:
            codigo = random.randint(100000, 999999)
            mensagem_email = "Seu código para validação de identidade e confirmação de senha é:"
            enviar_email(email_destinatario, codigo, mensagem_email)
            
            for tentativa in range(3):
                codigo_digitado = input("Digite o código de verificação enviado por email: ").strip()
                if codigo_digitado == str(codigo):
                    print("Código correto! Operação confirmada")
                    return senha
                print(f"Código incorreto. Tente novamente ({2-tentativa} tentativas restantes)")
            
            print("Número máximo de tentativas para o código excedido")
            return None
        print("As senhas não coincidem. Tente novamente")


#Gerenciamento de usuários 

#verifica se o e-mail já existe no arquivo de usuários
def email_ja_cadastrado(email):
    try:
        with open(ARQUIVO_USUARIOS, "r", encoding="utf-8") as arquivo:
            for linha in arquivo:
                if linha.strip().startswith(email + ";"):
                    return True
    except FileNotFoundError:
        pass
    return False

#realiza o cadastro de um novo usuário
def cadastrar_usuario():
    limpar_terminal()
    print("Cadastro de Usuário\n")
    email = validar_email()

    if email_ja_cadastrado(email):
        print("\nEste email já está cadastrado. Redirecionando...")
        time.sleep(2)
        limpar_terminal()
        return None

    senha = validar_senha(email)
    if senha:
        try:
            with open(ARQUIVO_USUARIOS, "a", encoding="utf-8") as arquivo:
                arquivo.write(f"{email};{senha}\n")
            print("\n✅ Cadastro realizado com sucesso!")
            pausar_e_limpar()
            return email
        except IOError:
            print("\n❌ Erro ao salvar usuário")
            pausar_e_limpar()
            return None
    else:
        print("\n❌ Falha no cadastro (código ou senha)")
        pausar_e_limpar()
        return None

#Realiza o login do usuário
def login():
    limpar_terminal()
    print("Login\n")
    email = input("Email: ").strip().lower()
    senha_digitada = input("Senha: ").strip()

    try:
        with open(ARQUIVO_USUARIOS, "r", encoding="utf-8") as arquivo:
            for linha in arquivo:
                e_arquivo, s_arquivo = linha.strip().split(";", 1)
                if e_arquivo == email and s_arquivo == senha_digitada:
                    print("\n✅ Login bem-sucedido!")
                    return email  
    except FileNotFoundError:
        print("Nenhum usuário cadastrado. Registre-se primeiro")
        return None
    except ValueError: 
        print("\n❌ Formato de arquivo de usuário inválido") 
        return None
    
    print("\n❌ Email ou senha inválidos")
    return None

#permite que um usuário redefina sua senha
def redefinir_senha():
    limpar_terminal()
    print("Recuperar conta\n")
    email = validar_email()

    if not email_ja_cadastrado(email):
        print("❌ Email não encontrado")
        pausar_e_limpar()
        return

    codigo_redefinicao = random.randint(100000, 999999)
    mensagem_email = "Seu código para redefinição de senha é:"
    enviar_email(email, codigo_redefinicao, mensagem_email)

    for tentativa_codigo in range(3):
        codigo_digitado = input("Digite o código enviado ao seu email para redefinir a senha: ").strip()
        if codigo_digitado == str(codigo_redefinicao):
            print("✅ Código correto.\nAgora, crie uma nova senha")
            nova_senha = validar_senha(email) 
            if nova_senha:
                try:
                    with open(ARQUIVO_USUARIOS, "r", encoding="utf-8") as f_leitura:
                        linhas = f_leitura.readlines()
                    
                    with open(ARQUIVO_USUARIOS, "w", encoding="utf-8") as f_escrita:
                        for linha_atual in linhas:
                            if linha_atual.strip().startswith(email + ";"):
                                f_escrita.write(f"{email};{nova_senha}\n")
                            else:
                                f_escrita.write(linha_atual)
                    print("✅ Senha redefinida com sucesso!")
                except IOError:
                    print("Erro ao redefinir senha no arquivo")
                finally:
                    pausar_e_limpar()
                    return
            else:
                print("❌ Falha ao criar a nova senha. A senha não foi alterada")
                pausar_e_limpar()
                return
        print(f"❌ Código incorreto. Tentativas restantes: {2-tentativa_codigo}")
            
    print("Número máximo de tentativas excedido. A senha não foi alterada")
    pausar_e_limpar()


#Funções Perfil de investidor

#coleta as respostas do usuário para o questionário de perfil
def pedir_respostas_investidor():
    limpar_terminal()
    print("Perfil de Investidor\n")
    input("Vamos descobrir o seu perfil de investidor. Pressione Enter para começar...")
    print("\nResponda com números de 1 a 5 para cada pergunta")

    perguntas = [
        "Disposição a correr riscos (1: Nenhuma - 5: Total): ",
        "Nível de Experiência com investimentos (1: Nenhuma - 5: Muita): ",
        "Necessidade de liquidez (1: Muito alta - 5: Muito baixa): "
    ]
    respostas = {}
    for i, pergunta_texto in enumerate(perguntas):
        while True:
            try:
                resposta_num = int(input(f"\n{i+1}. {pergunta_texto}"))
                if 1 <= resposta_num <= 5:
                    respostas[PROFILE_KEYS_ORDER[i]] = resposta_num
                    break
                print("Por favor, digite um número entre 1 e 5")
            except ValueError:
                print("Entrada inválida. Digite um número inteiro")
    return respostas

#determina o perfil (numérico e textual) com base nas respostas
def definir_perfil_investidor(respostas_investidor):
    if not respostas_investidor or len(respostas_investidor) != len(PROFILE_KEYS_ORDER):
        return None, "Perfil não definido"
    
    media = sum(respostas_investidor.values()) / len(respostas_investidor)
    perfil_num = round(media)
    perfis_map = {1: "Muito Conservador", 2: "Conservador", 3: "Moderado", 4: "Agressivo", 5: "Insano"}
    return perfil_num, perfis_map.get(perfil_num, "Desconhecido")

#salva ou atualiza o perfil do investidor no arquivo
def salvar_perfil_investidor(email_usuario, respostas):
    linhas_existentes = []
    encontrou_perfil = False
    try:
        with open(ARQUIVO_PERFIS, "r", encoding="utf-8") as f:
            linhas_existentes = f.readlines()
    except FileNotFoundError:
        pass

    respostas_str = [str(respostas[key]) for key in PROFILE_KEYS_ORDER]
    nova_linha = f"{email_usuario};{';'.join(respostas_str)}\n"

    with open(ARQUIVO_PERFIS, "w", encoding="utf-8") as f:
        for linha in linhas_existentes:
            if linha.startswith(email_usuario + ";"):
                f.write(nova_linha)
                encontrou_perfil = True
            else:
                f.write(linha)
        if not encontrou_perfil:
            f.write(nova_linha)
    print("💾 Perfil de investidor salvo/atualizado!")

#carrega o perfil do investidor do arquivo
def carregar_perfil_investidor(email_usuario):
    try:
        with open(ARQUIVO_PERFIS, "r", encoding="utf-8") as arquivo:
            for linha in arquivo:
                partes = linha.strip().split(";")
                if partes[0] == email_usuario and len(partes) == len(PROFILE_KEYS_ORDER) + 1:
                    return {PROFILE_KEYS_ORDER[i]: int(partes[i+1]) for i in range(len(PROFILE_KEYS_ORDER))}
    except FileNotFoundError:
        pass
    return None

#mostra sugestões de alocação conforme o perfil e valor a investir
def exibir_recomendacoes(perfil_num, perfil_str):
    if perfil_num is None:
        print("Não é possível gerar recomendações sem um perfil definido")
        return
    
    print(f"\n📊 Seu Perfil de Investidor: {perfil_str} (Nível {perfil_num})")

    while True:
        try:
            valor_aporte = float(input("Qual o valor que você pretende investir? R$ "))
            if valor_aporte > 0: break
            print("Por favor, insira um valor positivo")
        except ValueError:
            print("Valor inválido. Use números (ex: 1000.50)")

    alocacoes_padrao = {
        1: {'Renda Fixa': 50, 'FIIs': 20, 'Ações': 5,  'Cripto': 0,  'Reserva de Emergência': 25},
        2: {'Renda Fixa': 40, 'FIIs': 25, 'Ações': 15, 'Cripto': 5,  'Reserva de Emergência': 15},
        3: {'Renda Fixa': 25, 'FIIs': 30, 'Ações': 25, 'Cripto': 10, 'Reserva de Emergência': 10},
        4: {'Renda Fixa': 10, 'FIIs': 25, 'Ações': 35, 'Cripto': 20, 'Reserva de Emergência': 10},
        5: {'Renda Fixa': 5,  'FIIs': 20, 'Ações': 40, 'Cripto': 30, 'Reserva de Emergência': 5}
    }
    alocacao_sugerida = alocacoes_padrao.get(perfil_num, {}).copy()

    print(f"\n💰 Sugestão de Alocação para R$ {valor_aporte:,.2f}:")
    if not alocacao_sugerida:
        print("Não há sugestão de alocação para este perfil")
        return

    for tipo, perc in alocacao_sugerida.items():
        print(f"   - {tipo}: {perc}% → R$ {valor_aporte * (perc/100):,.2f}")

    if input("\nDeseja personalizar a alocação? (s/n): ").strip().lower() == 's':
        print("\nDigite os percentuais desejados (total deve ser 100%):")
        while True:
            nova_alocacao = {}
            total_perc = 0.0
            for tipo_ativo in alocacao_sugerida.keys():
                while True:
                    try:
                        perc = float(input(f"{tipo_ativo} (%): "))
                        if 0 <= perc <= 100:
                            nova_alocacao[tipo_ativo] = perc
                            total_perc += perc
                            break
                        print("Percentual entre 0 e 100")
                    except ValueError:
                        print("Entrada inválida")
            
            if abs(total_perc - 100.0) > 0.01:
                print(f"\nA soma foi {total_perc:.2f}%. Deve ser 100%. Tente de novo\n")
            else:
                alocacao_sugerida = nova_alocacao
                break
        
        print("\nAlocação final do seu aporte:")
        for tipo, perc in alocacao_sugerida.items():
            print(f"- {tipo}: {perc:.2f}% → R$ {valor_aporte * (perc/100):,.2f}")

#Permite visualizar, atualizar perfil e ver recomendações
def gerenciar_perfil_e_recomendacoes(email_usuario):
    limpar_terminal()
    print("Meu Perfil de Investidor e Recomendações\n")
    respostas_atuais = carregar_perfil_investidor(email_usuario)

    if respostas_atuais:
        perfil_num, perfil_str = definir_perfil_investidor(respostas_atuais)
        print(f"Seu perfil atual: {perfil_str} (Nível {perfil_num})")
        print("Respostas fornecidas:")
        for chave, valor in respostas_atuais.items(): print(f"   - {chave}: {valor}")
        
        exibir_recomendacoes(perfil_num, perfil_str)
        
        print("\nOpções:")
        print("1 - Atualizar meu perfil (refazer questionário)")
        print("2 - Voltar ao menu anterior")
        if input("Escolha: ").strip() == '1':
            novas_respostas = pedir_respostas_investidor()
            salvar_perfil_investidor(email_usuario, novas_respostas)
            perfil_num_novo, perfil_str_novo = definir_perfil_investidor(novas_respostas)
            exibir_recomendacoes(perfil_num_novo, perfil_str_novo)
    else:
        print("Você ainda não tem um perfil de investidor")
        if input("Deseja criar um agora? (s/n): ").strip().lower() == 's':
            respostas_novas = pedir_respostas_investidor()
            salvar_perfil_investidor(email_usuario, respostas_novas)
            perfil_num_novo, perfil_str_novo = definir_perfil_investidor(respostas_novas)
            exibir_recomendacoes(perfil_num_novo, perfil_str_novo)
    pausar_e_limpar()

#exclui o perfil de investidor do usuário
def excluir_perfil_investidor_usuario(email_usuario):
    limpar_terminal()
    print("Excluir Perfil de Investidor\n")
    if input(f"Tem certeza que deseja excluir seu perfil, {email_usuario}? (s/n): ").strip().lower() == 's':
        linhas_existentes = []
        perfil_removido = False
        try:
            with open(ARQUIVO_PERFIS, "r", encoding="utf-8") as arquivo:
                linhas_existentes = arquivo.readlines()
        except FileNotFoundError:
            print("Nenhum arquivo de perfis para excluir")
            pausar_e_limpar()
            return

        try:
            with open(ARQUIVO_PERFIS, "w", encoding="utf-8") as arquivo:
                for linha in linhas_existentes:
                    if not linha.startswith(email_usuario + ";"):
                        arquivo.write(linha)
                    else:
                        perfil_removido = True
            print("🗑️ Perfil de investidor excluído" if perfil_removido else "Perfil não encontrado")
        except IOError:
            print("Erro ao tentar excluir o perfil")
    else:
        print("Exclusão cancelada")
    pausar_e_limpar()


#MENUS 

#menu principal para usuários logados
def menu_usuario_logado(email_usuario):
    limpar_terminal()
    while True:
        print(f"--- Bem-vindo(a), {email_usuario}! ---")
        print("\nMenu Principal:")
        print("1 - Meu Perfil de Investidor e Recomendações")
        print("2 - Excluir meu Perfil de Investidor")
        print("3 - Logout")
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1": gerenciar_perfil_e_recomendacoes(email_usuario)
        elif opcao == "2": excluir_perfil_investidor_usuario(email_usuario)
        elif opcao == "3":
            print("Fazendo logout...")
            time.sleep(1)
            limpar_terminal()
            break 
        else:
            print("Opção inválida")
            pausar_e_limpar()

#menu inicial de autenticação do sistema
def menu_principal_autenticacao():
    limpar_terminal()
    while True:
        print("Sistema de Análise de Perfil de Investidor") 
        print("\nMenu de Autenticação:")
        print("1 - Login")
        print("2 - Cadastrar-se")
        print("3 - Recuperar conta")
        print("4 - Sair do Sistema")
        opcao = input("\nEscolha uma opção: ").strip()

        if opcao == "1":
            email_logado = login()
            if email_logado:
                pausar_e_limpar()
                menu_usuario_logado(email_logado)
            else:
                input("\nPressione Enter para voltar ao menu...") 
                limpar_terminal()
        elif opcao == "2": cadastrar_usuario()
        elif opcao == "3": redefinir_senha()
        elif opcao == "4":
            print("\nEncerrando o sistema... Até logo! 👋")
            break
        else:
            print("Opção inválida. Tente novamente")
            pausar_e_limpar()


#execução 

if __name__ == "__main__":
    #garante que os arquivos de dados existam
    try:
        open(ARQUIVO_USUARIOS, "a", encoding="utf-8").close()
        open(ARQUIVO_PERFIS, "a", encoding="utf-8").close()
    except IOError:
        print("Alerta: Não foi possível verificar/criar arquivos de dados iniciais")

    menu_principal_autenticacao()