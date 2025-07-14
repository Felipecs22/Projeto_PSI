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
    
class NichoInvestimento:
    """Representa um nicho de investimento com suas características intrínsecas."""
    def __init__(self, nome: str, risco: int, experiencia: int, liquidez: int):
        self.nome = nome
        self.risco = risco
        self.experiencia_requerida = experiencia
        self.liquidez = liquidez

class AvaliadorPerfil:
    """Calcula a adequação de nichos de investimento com base nas respostas de um usuário."""
    def __init__(self, respostas_usuario: dict):
        self.risco_usuario = respostas_usuario.get("Tolerancia ao risco", 0)
        self.experiencia_usuario = respostas_usuario.get("Experiencia", 0)
        necessidade_liquidez = respostas_usuario.get("Necessidade de liquidez", 0)
        self.preferencia_liquidez = 6 - necessidade_liquidez

    def _calcular_pontuacao_nicho(self, nicho: NichoInvestimento) -> dict:
        """Calcula a pontuação de adequação para um único nicho."""
        adequacao_risco = 5 - abs(self.risco_usuario - nicho.risco)
        adequacao_experiencia = 5 - max(0, nicho.experiencia_requerida - self.experiencia_usuario)
        adequacao_liquidez = 5 - abs(self.preferencia_liquidez - nicho.liquidez)
        pontuacao_total = adequacao_risco + adequacao_experiencia + adequacao_liquidez
        return {"nicho": nicho.nome, "pontuacao": pontuacao_total}

    def gerar_ranking(self, lista_nichos: list) -> list:
        """Recebe uma lista de nichos, calcula a pontuação e retorna um ranking ordenado."""
        resultados = [self._calcular_pontuacao_nicho(nicho) for nicho in lista_nichos]
        return sorted(resultados, key=lambda x: x["pontuacao"], reverse=True)