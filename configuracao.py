import os
from dotenv import load_dotenv


def carregar_token():
    """
    Esta função busca a "chave secreta" (token) do robô guardada no arquivo .env.
    Pense nela como se fosse pegar a chave certa no chaveiro para abrir a porta do Telegram.
    """
    # Lê as anotações do arquivo .env que está na mesma pasta do projeto
    load_dotenv()

    # Pega o valor da chave chamada TELEGRAM_TOKEN
    token = os.getenv("TELEGRAM_TOKEN")

    # Verifica se a pessoa esqueceu de colocar o token ou deixou o texto de exemplo
    if not token or token == "COLE_SEU_TOKEN_AQUI":
        print("\n" + "=" * 60)
        print("Atenção: Você ainda não configurou o token do seu robô!")
        print("1. Abra o arquivo '.env' neste mesmo diretório.")
        print("2. Cole lá o token que você recebeu do @BotFather no Telegram.")
        print("3. Salve o arquivo e tente rodar o programa novamente.")
        print("=" * 60 + "\n")
        raise SystemExit(1)

    return token
