import smtplib
from email.message import EmailMessage
import os
from dotenv import load_dotenv

# carrega as variáveis do arquivo .env para o ambiente do sistema
load_dotenv()

# pegando as variáveis 
EMAIL_REMETENTE = os.getenv("EMAIL_REMETENTE", "")
SENHA_APP = os.getenv("SENHA_APP", "")

print("--- INICIANDO DEBUG DE CREDENCIAIS ---")
print(f"E-mail que será usado: {EMAIL_REMETENTE}")
print(f"Senha de App foi lida do .env? {'Sim' if SENHA_APP else 'NÃO'}")
print(f"Comprimento da Senha lida: {len(SENHA_APP) if SENHA_APP else 0}")
print("--------------------------------------")

class ServicoEmail:
    """ classe com a lógica de envio de emails"""
    def __init__(self):
        self.remetente = EMAIL_REMETENTE
        self.senha = SENHA_APP
        self.host = "smtp.gmail.com"
        self.port = 465

    def enviar_email(self, destinatario, assunto, conteudo):
        """Método genérico para enviar um e-mail."""
        msg = EmailMessage()
        msg["Subject"] = assunto
        msg["From"] = self.remetente
        msg["To"] = destinatario
        msg.set_content(conteudo)

        try:
            with smtplib.SMTP_SSL(self.host, self.port) as smtp:
                smtp.login(self.remetente, self.senha)
                smtp.send_message(msg)
            print(f"E-mail de verificação enviado para {destinatario}!")
            return True
        except Exception as e:
            print(f"Falha ao enviar e-mail: {e}")
            return False