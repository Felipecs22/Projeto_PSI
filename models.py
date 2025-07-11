import re

class Usuario:
    """Representa um usuário com seus dados e comportamentos próprios."""
    def __init__(self, email, senha, id=None):
        if not self._is_formato_valido(email):
            raise ValueError("Formato de e-mail inválido.")
        self.id = id
        self.email = email
        self.senha = senha 

    def _is_formato_valido(self, email_a_verificar):
        return re.fullmatch(r"[^@]+@[^@]+\.[^@]+", email_a_verificar)
    
    def __str__(self):
        return f"Usuário(id={self.id}, email='{self.email}')"