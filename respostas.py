# -*- coding: utf-8 -*-
import re
import unicodedata
from datetime import datetime

ARQUIVO_LOG = "conversas_ecobot.log"

RESPOSTAS = {
    "saudacao": (
        "Olá! ♻️ Sou o EcoBot! Posso ajudar você "
        "a separar o lixo e cuidar do meio ambiente."
    ),
    "papel": (
        "🔵 PAPEL: descarte na lixeira azul.\n"
        "Exemplos: jornais, revistas, caixas e folhas "
        "de papel limpas e secas."
    ),
    "plastico": (
        "🔴 PLÁSTICO: descarte na lixeira vermelha.\n"
        "Exemplos: garrafas PET, embalagens e "
        "sacolas plásticas recicláveis."
    ),
    "vidro": (
        "🟢 VIDRO: descarte na lixeira verde.\n"
        "Exemplos: garrafas, potes e frascos de vidro.\n"
        "Cuidado com vidros quebrados! Embale com segurança."
    ),
    "metal": (
        "🟡 METAL: descarte na lixeira amarela.\n"
        "Exemplos: latas de refrigerante, latinhas "
        "e latas de alimentos."
    ),
    "organico": (
        "🟤 ORGÂNICO: descarte na lixeira marrom.\n"
        "Exemplos: restos de frutas, verduras e alimentos.\n"
        "Alguns resíduos podem virar adubo por compostagem."
    ),
    "pilhas": (
        "🔋 Pilhas e baterias não devem ir para "
        "o lixo comum.\n"
        "Leve até um ponto de coleta específico."
    ),
    "oleo": (
        "🛢️ Óleo de cozinha usado não deve ser "
        "jogado na pia.\n"
        "Guarde em uma garrafa fechada e leve "
        "a um ponto de coleta."
    ),
    "eletronicos": (
        "💻 Lixo eletrônico precisa de descarte especial.\n"
        "Exemplos: celulares, computadores e carregadores.\n"
        "Procure pontos de coleta de eletrônicos."
    ),
    "reciclagem": (
        "♻️ Reciclagem é transformar materiais usados "
        "em novos produtos.\n"
        "Ela ajuda a reduzir o lixo e preservar "
        "os recursos naturais."
    ),
    "coleta_seletiva": (
        "🌎 Coleta seletiva é separar os resíduos "
        "por tipo de material.\n"
        "Isso facilita a reciclagem e ajuda "
        "a proteger o meio ambiente."
    ),
    "cores": (
        "🎨 CORES DAS LIXEIRAS:\n"
        "🔵 Azul - Papel\n"
        "🔴 Vermelha - Plástico\n"
        "🟢 Verde - Vidro\n"
        "🟡 Amarela - Metal\n"
        "🟤 Marrom - Orgânicos\n"
        "⚪ Cinza - Resíduos não recicláveis"
    ),
    "meio_ambiente": (
        "🌱 Cuidar do meio ambiente ajuda "
        "a diminuir a poluição e proteger "
        "os animais, as plantas e os rios."
    ),
    "ajuda": (
        "♻️ Você pode perguntar sobre:\n"
        "- Papel, plástico, vidro e metal\n"
        "- Orgânicos, pilhas e baterias\n"
        "- Óleo de cozinha e eletrônicos\n"
        "- Cores das lixeiras\n"
        "- Coleta seletiva e reciclagem\n"
        "Digite sua dúvida!"
    ),
    "despedida": (
        "🌱 EcoBot: Obrigado por ajudar "
        "o meio ambiente!\n"
        "Até a próxima! ♻️"
    )
}

PALAVRAS_CHAVE = {
    "saudacao": ["oi", "ola", "bom dia", "boa tarde", "boa noite", "tudo bem"],
    "papel": ["papel", "papelao", "jornal", "revista", "caderno", "folha"],
    "plastico": ["plastico", "pet", "sacola", "garrafa pet", "embalagem plastica"],
    "vidro": ["vidro", "garrafa de vidro", "pote de vidro", "vidro quebrado"],
    "metal": ["metal", "aluminio", "latinha", "lata", "lata de refrigerante"],
    "organico": ["organico", "casca", "restos de comida", "fruta", "verdura", "compostagem"],
    "pilhas": ["pilha", "pilhas", "bateria", "baterias"],
    "oleo": ["oleo", "oleo de cozinha", "oleo usado"],
    "eletronicos": ["eletronicos", "eletronico", "eletrodomesticos", "eletrodomestico", "celular", "computador", "carregador", "notebook", "fios", "fio"],
    "reciclagem": ["reciclagem", "reciclar", "reciclavel", "reaproveitar"],
    "coleta_seletiva": ["coleta seletiva", "separar lixo", "separacao do lixo"],
    "cores": ["cores", "cor das lixeiras", "lixeiras", "qual lixeira"],
    "meio_ambiente": ["meio ambiente", "natureza", "poluicao", "planeta", "sustentabilidade"],
    "ajuda": ["ajuda", "menu", "opcoes", "o que voce faz"],
    "despedida": ["tchau", "xau", "ate logo", "ate mais", "obrigado", "obrigada", "ok", "baybay"]
}

def normalizar_texto(texto):
    texto = texto.lower().strip()
    texto = unicodedata.normalize("NFD", texto)
    texto = "".join(letra for letra in texto if unicodedata.category(letra) != "Mn")
    texto = re.sub(r"[^\w\s]", " ", texto)
    texto = re.sub(r"\s+", " ", texto)
    return texto.strip()

def tokenizar(texto):
    return texto.split()

def detectar_padrao(texto):
    padrao = r"(?:qual|que)\s+(?:e\s+a\s+)?cor"
    if re.search(padrao, texto):
        return "cores"
    padrao = r"(?:onde|como)\s+(?:eu\s+)?(?:descarto|descartar|jogo|jogar)"
    if re.search(padrao, texto):
        return "descarte"
    return None

def identificar_intencao(tokens, texto):
    frase = " ".join(tokens)
    if "coleta seletiva" in frase:
        return "coleta_seletiva"
    if "cores das lixeiras" in frase:
        return "cores"
    for intencao, palavras in PALAVRAS_CHAVE.items():
        if intencao in ["saudacao", "despedida"]:
            continue
        for palavra in palavras:
            palavra = normalizar_texto(palavra)
            if re.search(r"\b" + re.escape(palavra) + r"\b", frase):
                return intencao
    padrao = detectar_padrao(frase)
    if padrao == "cores":
        return "cores"
    for intencao in ["saudacao", "despedida"]:
        for palavra in PALAVRAS_CHAVE[intencao]:
            palavra = normalizar_texto(palavra)
            if re.search(r"\b" + re.escape(palavra) + r"\b", frase):
                return intencao
    return None

def resposta_fallback():
    return (
        "❌ Desculpe, não consegui entender sua pergunta.\n"
        "Tente perguntar de outra maneira.\n"
        "Exemplos:\n"
        "- Onde descartar papel?\n"
        "- Como reciclar plástico?\n"
        "- Onde jogar pilhas?\n"
        "- Quais são as cores das lixeiras?\n"
        "Digite 'ajuda' para ver mais opções."
    )

def registrar_log(mensagem, intencao, resposta):
    data_hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    with open(ARQUIVO_LOG, "a", encoding="utf-8") as arquivo:
        arquivo.write(f"[{data_hora}]\nUsuário: {mensagem}\nIntenção: {intencao}\nEcoBot: {resposta}\n\n")

def processar_mensagem(mensagem):
    texto = normalizar_texto(mensagem)
    tokens = tokenizar(texto)
    intencao = identificar_intencao(tokens, texto)
    if intencao is not None:
        resposta = RESPOSTAS[intencao]
    else:
        intencao = "desconhecida"
        resposta = resposta_fallback()
    registrar_log(mensagem, intencao, resposta)
    return resposta

# --- FUNÇÕES EXIGIDAS PELO TELEGRAM ---
async def responder_inicio(update, context):
    """Função chamada ao enviar /start"""
    resposta = RESPOSTAS["saudacao"] + "\n\n" + RESPOSTAS["ajuda"]
    await update.message.reply_text(resposta)

async def responder_ajuda(update, context):
    """Função chamada ao enviar /ajuda ou /help"""
    await update.message.reply_text(RESPOSTAS["ajuda"])

async def responder_conversa(update, context):
    """Função chamada quando o utilizador envia qualquer texto comum"""
    texto_usuario = update.message.text
    resposta = processar_mensagem(texto_usuario)
    await update.message.reply_text(resposta)