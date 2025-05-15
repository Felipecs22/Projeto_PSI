# Nível de tolerância ao risco
print("Qual o seu perfil de risco? (1) Conservador, (2) Moderado, (3) Agressivo")
perfil_risco = (input("Escolha 1, 2 ou 3: "))

# Frequência do aporte
print("Qual a frequência dos seus aportes? (1) Mensal, (2) Semanal, (3) Anual, (4) Único")
frequencia_aporte = (input("Escolha 1, 2, 3 ou 4: "))

# Valor do aporte
valor_aporte = (input("Qual o valor que você pretende investir? "))

# Tipos de investimentos desejados
print("Qual tipo de investimento você deseja incluir? (1) Ações, (2) Fundos Imobiliários, (3) Renda Fixa, (4) Outros")
tipos_investimentos = input("Escolha 1, 2, 3 ou 4 ")

# Alocações de exemplo para cada perfil de risco
alocacoes = {
    1: {'Renda Fixa': 70, 'FIIs': 20, 'Ações': 10},   # Conservador
    2: {'Renda Fixa': 40, 'FIIs': 30, 'Ações': 30},   # Moderado
    3: {'Renda Fixa': 20, 'FIIs': 30, 'Ações': 50}    # Agressivo
}

# Converter a escolha do usuário para nomes
mapa_tipos = {1: 'Ações', 2: 'FIIs', 3: 'Renda Fixa', 4: 'Outros'}