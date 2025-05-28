import re
import random
import time
import smtplib
from email.message import EmailMessage
import os

#definições
arquivo_perfis = "perfis_investidores.txt"
email_remetente = "fcsantos2201@gmail.com"  #email que vai interagir com user
senha_app = "zvwjliixtnnwkirm"  #senha app gmail
arquivo_usuarios = "usuarios.txt" #arquivo email+senha
ordem_lista = ["Tolerancia ao risco", "Experiencia", "Necessidade de liquidez"] #ordenando lista perfil



#Funções gerais

#Envia um e-mail com código de segurança
def enviar_email(destinatario, codigo, info_mensagem):
    msg = EmailMessage()
    msg["Subject"] = "Sistema de Autenticação - Código de segurança"
    msg["From"] = email_remetente
    msg["To"] = destinatario
    msg.set_content(f"{info_mensagem} {codigo}")

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(email_remetente, senha_app)
        smtp.send_message(msg)
    print(" Código de verificação enviado para o seu email!")

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
        senha = input("Crie sua nova senha (pelo menos 8 caracteres, com: pelo menos 1 número e uma letra maiúscula e minúscula. Ex: Codigo321): ").strip()

        if not senha.isalnum():
            print("Senha inválida. Use apenas letras e números")
            continue

        if not (len(senha) >= 8 and re.search(r"[A-Z]", senha) and re.search(r"[a-z]", senha) and re.search(r"[0-9]", senha)):
            print("Senha inválida. Deve ter pelo menos 8 caracteres, maiúscula, minúscula e número")
            continue

        confirmar_senha = input("Confirme sua senha: ").strip()
        if confirmar_senha == senha:
            codigo = random.randint(100000, 999999)
            mensagem_email = "Seu código para validação de identidade e confirmação de senha é:"
            enviar_email(email_destinatario, codigo, mensagem_email)

            for tentativa in range(5):
                codigo_digitado = input("Digite o código de verificação enviado por email: ").strip()
                if codigo_digitado == str(codigo):
                    print("Código correto! Operação confirmada")
                    return senha
                print(f"Código incorreto. Tente novamente ({4-tentativa} tentativas restantes)")

            print("Máximo de tentativas para o código excedido")
            return None
        print("As senhas não coincidem. Tente novamente")




#Gerenciamento de usuários

#verifica se o e-mail já existe no arquivo de usuários
def email_ja_cadastrado(email):
    if not os.path.exists(arquivo_usuarios):
        return False

    with open(arquivo_usuarios, "r", encoding="utf-8") as arquivo:
        for linha in arquivo:
            if linha.strip().startswith(email + ";"):
                return True
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
        with open(arquivo_usuarios, "a", encoding="utf-8") as arquivo:
            arquivo.write(f"{email};{senha}\n")
        print("\nCadastro realizado com sucesso!")
        pausar_e_limpar()
        return email
    else:
        print("\nFalha no cadastro (código ou senha)")
        pausar_e_limpar()
        return None

#Realiza o login do usuário
def login():
    limpar_terminal()
    print("Login\n")
    email = input("Email: ").strip().lower()
    senha_digitada = input("Senha: ").strip()

    if not os.path.exists(arquivo_usuarios):
        print("Nenhum usuário cadastrado. Registre-se primeiro")
        return None

    with open(arquivo_usuarios, "r", encoding="utf-8") as arquivo:
        for linha in arquivo:
            try:
                e_arquivo, s_arquivo = linha.strip().split(";", 1)
                if e_arquivo == email and s_arquivo == senha_digitada:
                    print("\nLogin bem-sucedido!")
                    return email
            except ValueError:
                continue 
    print("\nEmail ou senha inválidos")
    return None

#permite que um usuário redefina sua senha
def redefinir_senha():
    limpar_terminal()
    print("Recuperar conta\n")
    email = validar_email()

    if not email_ja_cadastrado(email):
        print("Email não encontrado")
        pausar_e_limpar()
        return

    codigo_redefinicao = random.randint(100000, 999999)
    mensagem_email = "Seu código para redefinição de senha é:"
    enviar_email(email, codigo_redefinicao, mensagem_email)

    for tentativa_codigo in range(3):
        codigo_digitado = input("Digite o código enviado ao seu email para redefinir a senha: ").strip()
        if codigo_digitado == str(codigo_redefinicao):
            print("Código correto.\nAgora, crie uma nova senha")
            nova_senha = validar_senha(email)
            if nova_senha:
                linhas_atualizadas = [] 
                with open(arquivo_usuarios, "r", encoding="utf-8") as f_leitura:
                    linhas = f_leitura.readlines()

                for linha_atual in linhas:
                    if linha_atual.strip().startswith(email + ";"):
                        linhas_atualizadas.append(f"{email};{nova_senha}\n")
                    else:
                        linhas_atualizadas.append(linha_atual)
                
                with open(arquivo_usuarios, "w", encoding="utf-8") as f_escrita:
                    f_escrita.writelines(linhas_atualizadas) 

                print("Senha redefinida com sucesso!")
                pausar_e_limpar()
                return
            else:
                print("Falha ao criar a nova senha. A senha não foi alterada")
                pausar_e_limpar()
                return
        print(f"Código incorreto. Tentativas restantes: {2-tentativa_codigo}")

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
            resposta_num_str = input(f"\n{i+1}. {pergunta_texto}").strip() 
            if resposta_num_str.isdigit():
                resposta_num = int(resposta_num_str)
                if 1 <= resposta_num <= 5:
                    respostas[ordem_lista[i]] = resposta_num
                    break
                else:
                    print("Por favor, digite um número entre 1 e 5")
            else:
                print("Entrada inválida. Digite um número inteiro")
    return respostas

#determina o perfil (numérico e textual) com base nas respostas
def definir_perfil_investidor(respostas_investidor):
    if not respostas_investidor or len(respostas_investidor) != len(ordem_lista):
        return None, "Perfil não definido"

    media = sum(respostas_investidor.values()) / len(respostas_investidor)
    perfil_nota = round(media)
    
    perfil_nota = max(1, min(5, perfil_nota))

    perfis_map = {1: "Muito Conservador", 2: "Conservador", 3: "Moderado", 4: "Agressivo", 5: "Insano"}
    return perfil_nota, perfis_map.get(perfil_nota, "Desconhecido")

#salva ou atualiza o perfil do investidor no arquivo
def salvar_perfil_investidor(email_usuario, respostas):
    linhas_existentes = []
    encontrou_perfil = False

    if os.path.exists(arquivo_perfis):
        with open(arquivo_perfis, "r", encoding="utf-8") as f:
            linhas_existentes = f.readlines()

    respostas_str_list = []
    for key in ordem_lista:
        respostas_str_list.append(str(respostas.get(key, ''))) 

    nova_linha = f"{email_usuario};{';'.join(respostas_str_list)}\n"
    
    linhas_para_escrever = []
    for linha in linhas_existentes:
        if linha.startswith(email_usuario + ";"):
            linhas_para_escrever.append(nova_linha)
            encontrou_perfil = True
        else:
            linhas_para_escrever.append(linha)
    
    if not encontrou_perfil:
        linhas_para_escrever.append(nova_linha)

    with open(arquivo_perfis, "w", encoding="utf-8") as f:
        f.writelines(linhas_para_escrever)
    print("Perfil de investidor salvo/atualizado!")

#carrega o perfil do investidor do arquivo
def carregar_perfil_investidor(email_usuario):
    if not os.path.exists(arquivo_perfis):
        return None

    with open(arquivo_perfis, "r", encoding="utf-8") as arquivo:
        for linha in arquivo:
            partes = linha.strip().split(";")
            if partes[0] == email_usuario and len(partes) == len(ordem_lista) + 1:
                try:
                    return {ordem_lista[i]: int(partes[i+1]) for i in range(len(ordem_lista))}
                except (ValueError, IndexError): 
                    return None 
    return None

# Função auxiliar para obter percentuais personalizados do usuário
def percentuais_personalizados(tipos_ativos_para_personalizar): # Nome alterado
    print("\nDigite os percentuais desejados (total deve ser 100%):")
    while True:
        nova_alocacao = {}
        total_perc = 0.0
        for tipo_ativo in tipos_ativos_para_personalizar:
            while True:
                perc_str = input(f"{tipo_ativo} (%): ").strip()
                try:
                    perc = float(perc_str)
                    if 0 <= perc <= 100:
                        nova_alocacao[tipo_ativo] = perc
                        total_perc += perc
                        break
                    else:
                        print("Percentual entre 0 e 100") 
                except ValueError:
                    print("Entrada inválida") 

        if abs(total_perc - 100.0) < 0.01: 
            return nova_alocacao
        else:
            print(f"\nA soma foi {total_perc:.2f}%. Deve ser 100%. Tente de novo\n")


#mostra sugestões de alocação conforme o perfil e valor a investir
def exibir_recomendacoes(perfil_nota, perfil_str):
    if perfil_nota is None:
        print("Não é possível gerar recomendações sem um perfil definido")
        return

    print(f"\nSeu Perfil de Investidor: {perfil_str} (Nível {perfil_nota})")

    while True:
        valor_aporte_str = input("Qual o valor que você pretende investir? R$ ").strip() 
        try:
            valor_aporte = float(valor_aporte_str)
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
    alocacao_sugerida = alocacoes_padrao.get(perfil_nota, {}).copy()

    print(f"\nSugestão de Alocação para R$ {valor_aporte:,.2f}:")
    if not alocacao_sugerida:
        print("Não há sugestão de alocação para este perfil")
        return

    for tipo, perc in alocacao_sugerida.items():
        print(f"    - {tipo}: {perc}% -> R$ {valor_aporte * (perc/100):,.2f}") 

    time.sleep(3) 

    if input("\nDeseja personalizar a alocação? (sim/não): ").strip().lower() == 'sim':
        tipos_para_personalizar = list(alocacao_sugerida.keys())
        if tipos_para_personalizar:
            alocacao_personalizada = percentuais_personalizados(tipos_para_personalizar) # Nome alterado na chamada
            alocacao_sugerida = alocacao_personalizada 
        else:
            print("Não há tipos de ativos para personalizar neste perfil.")


    print("\nAlocação final do seu aporte:")
    for tipo, perc in alocacao_sugerida.items():
        print(f"- {tipo}: {perc:.2f}% -> R$ {valor_aporte * (perc/100):,.2f}")

#Permite visualizar, atualizar perfil e ver recomendações
def gerenciar_perfil_e_recomendacoes(email_usuario):
    limpar_terminal()
    print("Meu Perfil de Investidor e Recomendações\n")
    respostas_atuais = carregar_perfil_investidor(email_usuario)

    if respostas_atuais:
        perfil_nota, perfil_str = definir_perfil_investidor(respostas_atuais)
        print(f"Seu perfil atual: {perfil_str} (Nível {perfil_nota})")
        print("Respostas fornecidas:")
        for chave, valor in respostas_atuais.items(): print(f"    - {chave}: {valor}") 

        exibir_recomendacoes(perfil_nota, perfil_str)

        print("\nOpções:")
        print("1 - Atualizar meu perfil (refazer questionário)")
        print("2 - Voltar ao menu anterior")
        escolha = input("Escolha: ").strip() 
        if escolha == '1':
            novas_respostas = pedir_respostas_investidor()
            salvar_perfil_investidor(email_usuario, novas_respostas)
            perfil_nota_novo, perfil_str_novo = definir_perfil_investidor(novas_respostas)
            exibir_recomendacoes(perfil_nota_novo, perfil_str_novo)
    else:
        print("Você ainda não tem um perfil de investidor")
        if input("Deseja criar um agora? (sim/não): ").strip().lower() == 'sim':
            respostas_novas = pedir_respostas_investidor()
            salvar_perfil_investidor(email_usuario, respostas_novas)
            perfil_nota_novo, perfil_str_novo = definir_perfil_investidor(respostas_novas)
            exibir_recomendacoes(perfil_nota_novo, perfil_str_novo)
    pausar_e_limpar()


#exclui o perfil de investidor do usuário
def excluir_perfil_investidor_usuario(email_usuario):
    limpar_terminal()
    print("Excluir Perfil de Investidor\n")
    if input(f"Tem certeza que deseja excluir seu perfil, {email_usuario}? (sim/não): ").strip().lower() == 'sim':
        linhas_existentes = []
        perfil_removido = False

        if not os.path.exists(arquivo_perfis):
            print("Nenhum arquivo de perfis para excluir")
            pausar_e_limpar()
            return

        with open(arquivo_perfis, "r", encoding="utf-8") as arquivo:
            linhas_existentes = arquivo.readlines()

        linhas_para_manter = [] 
        for linha in linhas_existentes:
            if not linha.startswith(email_usuario + ";"):
                linhas_para_manter.append(linha)
            else:
                perfil_removido = True
        
        if perfil_removido:
            with open(arquivo_perfis, "w", encoding="utf-8") as arquivo:
                arquivo.writelines(linhas_para_manter)
            print("Perfil de investidor excluído")
        else:
            print("Perfil não encontrado") 
    else:
        print("Exclusão cancelada")
    pausar_e_limpar()



#MENUS

#menu principal para usuários logados
def menu_usuario_logado(email_usuario):
    while True:
        limpar_terminal() 
        print(f"--- Bem-vindo(a), {email_usuario}! ---")
        print("\nMenu Principal:")
        print("1 - Meu Perfil de Investidor e Recomendações")
        print("2 - Excluir meu Perfil de Investidor")
        print("3 - Logout")
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1": 
            gerenciar_perfil_e_recomendacoes(email_usuario)
        elif opcao == "2": 
            excluir_perfil_investidor_usuario(email_usuario)
        elif opcao == "3":
            print("Fazendo logout...")
            time.sleep(1)
            break 
        else:
            print("Opção inválida")
            pausar_e_limpar()

#menu inicial de autenticação do sistema
def menu_principal_autenticacao():
    while True:
        limpar_terminal()
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
                menu_usuario_logado(email_logado)
            else:
                input("\nPressione Enter para voltar ao menu...")
        elif opcao == "2": 
            cadastrar_usuario() 
        elif opcao == "3": 
            redefinir_senha() 
        elif opcao == "4":
            print("\nEncerrando o sistema... Até logo!")
            time.sleep(1) 
            limpar_terminal()
            break
        else:
            print("Opção inválida. Tente novamente")
            pausar_e_limpar()



#execução


open(arquivo_usuarios, "a", encoding="utf-8").close()
open(arquivo_perfis, "a", encoding="utf-8").close()

menu_principal_autenticacao()