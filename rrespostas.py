from telegram import Update
from telegram.ext import ContextTypes


def criar_resposta_para_texto(mensagem_do_usuario: str) -> str:
    """
    Aqui fica o cérebro das conversas do robô!
    Ele olha o que a pessoa escreveu e escolhe a melhor resposta.
    Você pode adicionar novas palavras e frases aqui de forma bem simples.
    """
    # Deixa o texto em letras minúsculas para facilitar a comparação
    texto_limpo = mensagem_do_usuario.strip().lower()

    if texto_limpo in ["oi", "olá", "ola", "opa", "e aí"]:
        return "Olá! Que bom falar com você! Como posso te ajudar hoje?"

    if "tudo bem" in texto_limpo:
        return "Tudo ótimo por aqui! E com você, como estão as coisas?"

    if "quem é você" in texto_limpo or "quem e voce" in texto_limpo:
        return "Eu sou um robô de conversa criado em Python para o Telegram! 🤖"

    # Se o robô não conhecer a frase exata, ele responde com gentileza
    return (
        f'Você disse: "{mensagem_do_usuario}" 😊\n\n'
        "Eu ainda estou aprendendo novas frases! "
        "Envie /ajuda para ver o que já sei fazer."
    )


async def responder_inicio(atualizacao: Update, contexto: ContextTypes.DEFAULT_TYPE):
    """
    Esta função é chamada quando o usuário entra no chat e clica no botão "Começar" ou digita /start.
    Ela dá as boas-vindas e ensina os primeiros passos.
    """
    # Pega o primeiro nome da pessoa no Telegram para cumprimentá-la com carinho
    nome_do_usuario = atualizacao.effective_user.first_name

    mensagem_boas_vindas = (
        f"Olá, {nome_do_usuario}! 👋\n\n"
        "Seja muito bem-vindo(a) ao nosso Chatbot!\n"
        "Você pode conversar comigo enviando mensagens de texto ou usar os seguintes comandos:\n"
        "👉 /start - Reinicia esta conversa\n"
        "👉 /ajuda - Mostra a lista de comandos disponíveis\n\n"
        "Pode me mandar um 'oi' se quiser testar!"
    )

    # Envia a mensagem de resposta de volta para a conversa no Telegram
    await atualizacao.message.reply_text(mensagem_boas_vindas)


async def responder_ajuda(atualizacao: Update, contexto: ContextTypes.DEFAULT_TYPE):
    """
    Esta função é chamada quando alguém digita /ajuda ou /help.
    Ela explica tudo o que o robô sabe fazer.
    """
    texto_ajuda = (
        "ℹ️ *Como conversar comigo:*\n\n"
        "1. Escreva palavras comuns como 'oi', 'tudo bem?' ou 'quem é você?'.\n"
        "2. Se você escrever qualquer outra coisa, eu vou ler e te responder com atenção.\n"
        "3. Comandos especiais:\n"
        "   • /start - Dá as boas-vindas novamente\n"
        "   • /ajuda - Mostra este guia de ajuda"
    )

    # Envia o texto formatado para o usuário
    await atualizacao.message.reply_text(texto_ajuda)


async def responder_conversa(atualizacao: Update, contexto: ContextTypes.DEFAULT_TYPE):
    """
    Esta função é chamada automaticamente toda vez que alguém envia qualquer mensagem de texto comum.
    Ela lê o que foi escrito, pede uma resposta para a função 'criar_resposta_para_texto' e envia de volta.
    """
    # Lê o que o usuário escreveu no Telegram
    texto_recebido = atualizacao.message.text

    # Decide o que responder
    texto_resposta = criar_resposta_para_texto(texto_recebido)

    # Devolve a resposta na conversa
    await atualizacao.message.reply_text(texto_resposta)
