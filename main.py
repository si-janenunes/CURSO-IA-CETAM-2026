from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters

from configuracao import carregar_token
from respostas import responder_ajuda, responder_conversa, responder_inicio


def iniciar_robo():
    """
    Esta é a função principal que "liga o motor" do robô:
    1. Pega o token secreto para autorizar o robô no Telegram.
    2. Ensina o robô o que fazer para cada tipo de mensagem (comandos ou texto).
    3. Deixa o robô acordado e atento, esperando novas mensagens chegarem.
    """
    # 1. Busca a chave secreta no arquivo .env
    token = carregar_token()

    print("🤖 Ligando o robô do Telegram...")

    # 2. Cria a estrutura do robô usando a biblioteca oficial
    aplicativo = ApplicationBuilder().token(token).build()

    # 3. Ensina os comandos:
    # Quando alguém digitar /start, chame a função responder_inicio
    aplicativo.add_handler(CommandHandler("start", responder_inicio))

    # Quando alguém digitar /ajuda ou /help, chame a função responder_ajuda
    aplicativo.add_handler(CommandHandler("ajuda", responder_ajuda))
    aplicativo.add_handler(CommandHandler("help", responder_ajuda))

    # Quando alguém enviar qualquer texto que não seja um comando, chame responder_conversa
    aplicativo.add_handler(
        MessageHandler(filters.TEXT & (~filters.COMMAND), responder_conversa)
    )

    print("✅ Robô pronto e conectado com sucesso!")
    print("👉 Abra o seu aplicativo do Telegram e converse com o seu robô.")
    print("👉 Para parar o robô a qualquer momento, aperte as teclas Ctrl + C aqui no terminal.\n")

    # 4. Coloca o robô para ficar ouvindo as mensagens sem parar
    aplicativo.run_polling()


# Este bloco garante que o robô só comece a rodar se executarmos este arquivo diretamente
if __name__ == "__main__":
    iniciar_robo()
