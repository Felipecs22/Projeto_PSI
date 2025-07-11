# 📋 InvestiMatch

Este repositório contém um sistema de autenticação e análise de perfil de investidor, desenvolvido como um projeto prático de programação. Ele permite que os usuários criem e gerenciem suas contas, além de determinar seu perfil de investidor e receber sugestões de alocação de investimentos.

## 📚 Bibliotecas Utilizadas
O projeto utiliza as seguintes bibliotecas Python para suas funcionalidades:

###### os: Para interações com o sistema operacional, como a limpeza do terminal, proporcionando uma experiência de usuário mais limpa e intuitiva.

###### re: Para trabalhar com expressões regulares 📝, garantindo que os e-mails e senhas fornecidos pelos usuários sigam formatos específicos e seguros.

###### random: Utilizado para gerar códigos de verificação aleatórios 🎲 que são enviados por e-mail, adicionando uma camada extra de segurança nos processos de cadastro e redefinição de senha.

###### time: Permite introduzir pausas na execução do programa (time.sleep()) ⏳, melhorando a legibilidade e a interação ao dar tempo para o usuário ler mensagens importantes antes que a tela seja limpa.

###### smtplib: A biblioteca padrão do Python para enviar e-mails via protocolo SMTP 📧. É crucial para o envio dos códigos de segurança.

###### email.message: Uma classe útil para criar e formatar mensagens de e-mail ✉️, facilitando a definição de assunto, remetente, destinatário e conteúdo das mensagens enviadas.

## 🗂️ Organização dos Módulos
O projeto está organizado em um único arquivo Python, que encapsula todas as funcionalidades de autenticação, perfil de investidor e menus de navegação:

main.py (ou o nome do seu arquivo Python): Contém toda a lógica do programa, incluindo:

###### Utilitários: Funções de apoio como limpar_terminal() e enviar_email().

###### Validações (Autenticação): Funções para garantir o formato correto de e-mail e a complexidade da senha, além de lidar com a verificação de código por e-mail.

###### Gerenciamento de Usuários (Autenticação): Funções para cadastrar_usuario(), login() e redefinir_senha().

###### Gerenciamento de Perfil de Investidor: Funções para pedir_respostas_investidor(), definir_perfil_investidor(), salvar_perfil_investidor(), carregar_perfil_investidor(), exibir_recomendacoes() e excluir_perfil_investidor_usuario().

###### Menus de Navegação: Funções para guiar o usuário através das opções do sistema, como menu_usuario_logado() e menu_principal_autenticacao().

## ✨ Funcionalidades
O sistema oferece as seguintes funcionalidades principais:

###### Cadastro de Usuário 🧑‍💻: Novos usuários podem criar uma conta fornecendo e-mail e uma senha que atenda a critérios de segurança. Um código de verificação é enviado por e-mail para confirmar a autenticidade do cadastro.

###### Login de Usuário 🔑: Usuários cadastrados podem acessar o sistema com seu e-mail e senha.

###### Redefinição de Senha 🔄: Caso o usuário esqueça a senha, pode redefini-la através de um código de segurança enviado para seu e-mail, garantindo que apenas o proprietário da conta possa alterá-la.

###### Questionário de Perfil de Investidor 📝: Após o login, o usuário pode responder a um questionário simples para determinar seu perfil de investidor (de "Muito Conservador" a "Insano").

###### Recomendações de Alocação de Investimentos 📊: Com base no perfil do investidor e no valor de aporte mensal informado, o sistema sugere uma alocação percentual em diferentes tipos de ativos (Renda Fixa, FIIs, Ações, Cripto, Reserva de Emergência).

###### Personalização da Alocação ⚙️: O usuário tem a opção de ajustar manualmente os percentuais de alocação sugeridos, com validação para garantir que a soma total seja 100%.

###### Persistência de Dados 💾: As informações de usuários e perfis de investidor são salvas em arquivos de texto (usuarios.txt e perfis_investidores.txt), permitindo que os dados sejam mantidos entre as sessões.

###### Exclusão de Perfil de Investidor 🗑️: O usuário pode remover seu perfil de investidor do sistema.

## 💡 Inovação e Aplicação:
O InvestiMatch vai além da simples autenticação! Ele incorpora um sistema de análise de perfil de investidor, que, embora simplificado, demonstra como um aplicativo pode oferecer recomendações personalizadas com base nas respostas do usuário. A funcionalidade de salvar e carregar perfis, juntamente com as sugestões de alocação de investimentos, cria uma experiência de usuário mais rica e prática, abordando conceitos financeiros básicos de forma acessível.
