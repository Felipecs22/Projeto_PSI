import re

"""Classe para criar o objeto usuario
cria um usuário com seus dados e comportamentos próprios."""


class Usuario:

    def __init__(self, email, senha, id=None):

        # verifica se o formato é valido
        if not self.formato_valido(email):
            raise ValueError("Formato de e-mail inválido.")
        self.id = id
        self.email = email
        self.senha = senha

    def formato_valido(self, email_a_verificar):
        return re.fullmatch(r"[^@]+@[^@]+\.[^@]+", email_a_verificar)

    def __str__(self):
        return f"Usuário(id={self.id}, email='{self.email}')"


"""Classe para as carteiras de investimentos do usuario. representa uma carteira de investimentos de um usuário"""


class Carteira:

    def __init__(self, nome: str, usuario_id: int, id: int = None):

        self.id = id
        self.nome = nome
        self.usuario_id = usuario_id

    def __str__(self):
        """Define como o objeto Carteira será exibido ao ser 'printado'."""
        return f"Carteira(id={self.id}, nome='{self.nome}')"


"""Classe que cria os nichos de investimento"""
"""cria um nicho de investimento com suas características intrínsecas."""


class NichoInvestimento:

    def __init__(
        self,
        nome: str,
        risco: int,
        experiencia: int,
        liquidez: int,
        descricao: str,
        exemplos: str,
    ):
        self.nome = nome
        self.risco = risco
        self.experiencia_requerida = experiencia
        self.liquidez = liquidez
        self.descricao = descricao
        self.exemplos = exemplos


"""classe para caucular a adequação de nichos de investimento com base nas respostas de um usuário."""


class AvaliadorPerfil:  # A REGRA DE NEGOCIO TA AQUI

    def __init__(self, respostas_usuario: dict):
        # temos as respostas
        self.risco_usuario = respostas_usuario.get("Tolerancia ao risco", 0)
        self.experiencia_usuario = respostas_usuario.get("Experiencia", 0)
        necessidade_liquidez = respostas_usuario.get("Necessidade de liquidez", 0)
        # invertendo a escala para liquidez
        self.preferencia_liquidez = 6 - necessidade_liquidez

    def calcular_pontuacao_nicho(self, nicho: NichoInvestimento) -> dict:
        """Calcula a pontuação de adequação para um único nicho."""
        adequacao_risco = 5 - abs(self.risco_usuario - nicho.risco)
        # para exp pegamos o max entre a subtração e 0. A pontuação do nicho NÃO É PUNIDA se o usuario tiver uma exp maior q a requerida
        adequacao_experiencia = 5 - max(
            0, nicho.experiencia_requerida - self.experiencia_usuario
        )
        adequacao_liquidez = 5 - abs(self.preferencia_liquidez - nicho.liquidez)
        # pontuação total é a soma das 3. vai de 0 a 15
        pontuacao_total = adequacao_risco + adequacao_experiencia + adequacao_liquidez
        return {"nicho": nicho.nome, "pontuacao": pontuacao_total}

    def gerar_ranking(self, lista_nichos: list) -> list:
        """Recebe uma lista de nichos, calcula a pontuação e retorna um ranking ordenado."""
        resultados = [self.calcular_pontuacao_nicho(nicho) for nicho in lista_nichos]
        return sorted(resultados, key=lambda x: x["pontuacao"], reverse=True)
