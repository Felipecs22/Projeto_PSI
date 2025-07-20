# 📋 InvestiMatch

Cansado de planilhas confusas para acompanhar seus investimentos? O InvestiMatch nasceu como um projeto para simplificar essa jornada. Ele te ajuda a entender seu perfil de investidor, organiza seus aportes em diferentes carteiras e oferece recomendações personalizadas baseadas no seu comportamento.

É uma ferramenta construída para trazer clareza e organização ao mundo dos investimentos pessoais, evoluindo de um simples script para uma aplicação robusta e segura.

---

## ✨ O que o InvestiMatch faz?

* **Gestão de Múltiplas Carteiras 📂:** Crie carteiras separadas para diferentes objetivos, como "Aposentadoria", "Viagem dos Sonhos" ou "Reserva de Emergência", e organize seus investimentos de forma lógica.

* **Análise de Perfil de Investidor 🧠:** Através de um questionário simples, o sistema traça seu perfil de investidor para que você entenda melhor sua tolerância a riscos e seus objetivos.

* **Sistema de Recomendação Personalizado 🎯:** Com base no seu perfil, o aplicativo calcula uma pontuação de compatibilidade para diferentes classes de ativos (Renda Fixa, Ações, Cripto, etc.), ajudando a guiar suas decisões.

* **Registro de Aportes e Retiradas 📈:** Registre cada compra ou venda de ativos em suas respectivas carteiras. O sistema mantém um histórico detalhado e um resumo consolidado do valor total investido por ativo.

* **Autenticação Segura 🔐:** O sistema protege suas informações com um fluxo de autenticação completo, incluindo cadastro com verificação por e-mail, recuperação de conta e senhas armazenadas com hashing de segurança.

---

## 🗂️ Arquitetura e Filosofia do Projeto

O InvestiMatch evoluiu de um script único para uma arquitetura modular e orientada a objetos, onde cada parte do sistema é um "especialista" com uma única responsabilidade.

* **`main.py` (O Gerente 👔):** Orquestra a aplicação, controla os menus e o fluxo de interação com o usuário, mas delega as tarefas pesadas para os outros especialistas.

* **`database.py` (O Arquivista 🗄️):** É o único que sabe falar com o banco de dados. Todas as operações de leitura, escrita, atualização e exclusão de dados estão centralizadas aqui.

* **`models.py` (As Plantas Baixas 📐):** Define a estrutura dos nossos dados através de classes como `Usuario`, `Carteira` e `PerfilInvestidor`. Garante que os dados sejam tratados de forma organizada e consistente.

* **`servicos.py` (O Carteiro 📧):** Um especialista focado em uma única tarefa externa: enviar e-mails para verificação de conta e recuperação de senha.

* **`utils.py` (A Caixa de Ferramentas 🛠️):** Contém funções auxiliares e genéricas, como a limpeza do terminal ou a geração de hashes para senhas, que podem ser usadas por qualquer parte do sistema.

---

## 📚 Tecnologias Utilizadas

* **Python 3:** A linguagem principal do projeto.
* **SQLite3:** Para armazenar todos os dados de forma segura e organizada em um banco de dados local, substituindo os antigos arquivos de texto.
* **`hashlib`:** Para garantir a segurança das senhas dos usuários através de hashing.
* **`smtplib` e `email`:** Para a comunicação com o usuário via e-mail, de forma nativa.
* **`python-dotenv`:** Para proteger informações sensíveis (como senhas de e-mail), mantendo-as fora do código-fonte e em um ambiente seguro.
* **`os`, `re`, `random`, `time`:** Bibliotecas padrão do Python para diversas funcionalidades de apoio.

---

## 🚀 Como Executar o Projeto Localmente

1.  **Clone o Repositório:**
    ```bash
    git clone [https://github.com/Felipecs22/Projeto_PSI.git](https://github.com/Felipecs22/Projeto_PSI.git)
    ```

2.  **Navegue até a Pasta:**
    ```bash
    cd Projeto_PSI
    ```

3.  **Instale as Dependências:**
    O projeto tem uma dependência externa que precisa ser instalada.
    ```bash
    pip install python-dotenv
    ```

4.  **Configure suas Credenciais:**
    Crie um arquivo chamado `.env` na pasta raiz do projeto. Você pode copiar o arquivo `.env.example` (se houver) ou criar um novo com o seguinte conteúdo, preenchendo com suas informações:
    ```
    # Dentro do arquivo .env
    EMAIL_REMETENTE="seu-email-de-envio@gmail.com"
    SENHA_APP="sua-senha-de-app-de-16-letras"
    ```
    *Lembre-se que `SENHA_APP` deve ser uma "Senha de App" gerada na sua conta Google.*

5.  **Execute a Aplicação:**
    ```bash
    python main.py
    ```
    O programa irá inicializar o banco de dados (`investimatch.db`) na primeira execução e exibir o menu principal.
