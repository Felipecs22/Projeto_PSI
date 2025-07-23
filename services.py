import smtplib
from email.message import EmailMessage
import os
from dotenv import load_dotenv

load_dotenv()

#lendo credenciais
email_lido = os.getenv("EMAIL_REMETENTE")
senha_lida = os.getenv("SENHA_APP")

#tratamento de erro nas strings
EMAIL_REMETENTE = str(email_lido).strip() if email_lido else ""
SENHA_APP = str(senha_lida).strip() if senha_lida else ""

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