users = {}

while True:

    while True:
        
        email = input("Enter email: ")
        if '@' not in email:
            print('error. não tem @ no email')
            continue
        elif email in users:
            print("erro. email já em uso")
            continue
        elif ' ' in email:
            print('erro. tem espaço no email')
            continue
        if any(char in "!#$%&*+/=?^`{|}~" for char in email):
            print('erro. email não pode ter caracteres especiais')
            continue
        else:
            break

    while True:

        password = input("Digite senha: ")
        if 20<=len(password)<=8:
            print("erro. senha deve ter entre 8 e 20 caractéres")
            continue
        else:
            users[email] = password
            print(f"User criado com email: {email}")
            break
