# 📋 InvestiMatch

Este artigo apresenta o desenvolvimento do Investimatch, uma aplicação em Python voltada à organização de carteiras de investimento de forma personalizada. A plataforma identifica o perfil do investidor por meio de um questionário e, com base nas respostas, sugere uma alocação estratégica entre diferentes tipos de ativos. O sistema foi construído para auxiliar tanto iniciantes quanto investidores experientes, promovendo decisões mais conscientes e alinhadas ao perfil de risco individual.

---

## ✨ Funcionalidades Principais

* **Gestão de Múltiplas Carteiras 📂:** Crie e gerencie carteiras separadas para diferentes objetivos (ex: "Aposentadoria", "Reserva de Emergência") para uma organização financeira clara e eficaz.

* **Análise de Perfil de Investidor 🧠:** Através de um questionário intuitivo, o sistema identifica o perfil de risco do usuário, um pilar fundamental para uma tomada de decisão segura no mercado financeiro.

* **Recomendação e Alocação Estratégica 🎯:** O sistema gera uma sugestão de alocação de ativos com base no perfil identificado, traduzindo as respostas do usuário em um ranking de compatibilidade e uma distribuição percentual clara e educativa.

* **Registro de Aportes e Retiradas 📈:** Registre cada transação em suas respectivas carteiras. O sistema mantém um histórico detalhado (extrato de movimentações) e um resumo consolidado do valor total por ativo.

* **Autenticação Segura 🔐:** O sistema protege as informações com um fluxo de autenticação completo, incluindo cadastro com verificação por e-mail, recuperação de conta, exclusão de conta e senhas armazenadas com hashing de segurança.

---

## 🗂️ Arquitetura do Projeto

O InvestiMatch foi desenvolvido utilizando os princípios da programação orientada a objetos, o que facilitou a organização, reuso e manutenção do código. A arquitetura modular garante que cada parte do sistema tenha uma responsabilidade clara:

* **`main.py` (O Gerente 👔):** Orquestra a aplicação, controla os menus e o fluxo de interação com o usuário.
* **`database.py` (O Arquivista 🗄️):** Centraliza toda a comunicação com o banco de dados SQLite, gerenciando as operações de leitura e escrita.
* **`models.py` (As Plantas Baixas 📐):** Define a estrutura dos dados através de classes como `Usuario`, `Carteira` e `PerfilInvestidor`.
* **`servicos.py` (O Carteiro 📧):** Isola a comunicação com serviços externos, como o envio de e-mails via SMTP.
* **`utils.py` (A Caixa de Ferramentas 🛠️):** Contém funções auxiliares e genéricas, como a limpeza do terminal e a geração de hashes para senhas.

---

## 📚 Tecnologias Utilizadas

* **Python 3:** A linguagem principal do projeto, escolhida por sua clareza e vasto ecossistema.
* **SQLite3:** Para armazenar todos os dados de forma segura e organizada em um banco de dados local.
* **`hashlib`:** Para garantir a segurança das senhas dos usuários através de hashing.
* **`smtplib` e `email.message`:** Para a comunicação com o usuário via e--mail de forma nativa.
* **`python-dotenv`:** Para proteger informações sensíveis, mantendo-as fora do código-fonte.
* **Git:** Ferramenta de controle de versões utilizada para acompanhar as mudanças no código e permitir a colaboração segura.
* **Bibliotecas Padrão:** `os`, `re`, `random`, `datetime`.

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

3.  **Crie e Ative um Ambiente Virtual:**
    ```bash
    # Criar o ambiente
    python -m venv .venv
    # Ativar no Windows
    .venv\Scripts\activate
    # Ativar no macOS/Linux
    # source .venv/bin/activate
    ```

4.  **Instale as Dependências:**
    Use o arquivo `requirements.txt` para instalar as bibliotecas necessárias.
    ```bash
    pip install -r requirements.txt
    ```

5.  **Configure suas Credenciais:**
    Crie um arquivo chamado `.env` na pasta raiz do projeto. Preencha com suas informações de e-mail e Senha de App do Google:
    ```
    # Dentro do arquivo .env
    EMAIL_REMETENTE="seu-email-de-envio@gmail.com"
    SENHA_APP="sua-senha-de-app-de-16-letras"
    ```

6.  **Execute a Aplicação:**
    ```bash
    python main.py
    ```
    O programa irá inicializar o banco de dados e exibir o menu principal.

---

## 👥 Autores

* **Arthur Alves** - `arthurasantos.pro@gmail.com`
* **Felipe Santos** - `fcsantos201@gmail.com`
