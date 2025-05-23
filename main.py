import time
import requests
import telegram

# Token do bot e ID do chat
TOKEN = "7886005192:AAExBYx3YaXsXH4I71rePSdGThS7asmO93s"
CHAT_ID = "855971772"

# Inicializa o bot do Telegram
bot = telegram.Bot(token=TOKEN)

# Função para buscar novos tokens do Pump.fun
def fetch_new_tokens():
    try:
        response = requests.get("https://client-api.pump.fun/tokens/")
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        print(f"Erro ao buscar tokens: {e}")
    return []

sent_tokens = set()

# Loop principal
while True:
    tokens = fetch_new_tokens()
    for token in tokens:
        address = token.get("address")
        if address in sent_tokens:
            continue

        twitter = token.get("twitter", "").strip()
        telegram_link = token.get("telegram", "").strip()

        if twitter and telegram_link:
            name = token.get("name", "Sem nome")
            message = (
                f"🚀 Novo Token no Pump.fun!

"
                f"🪙 Nome: {name}
"
                f"📬 Endereço: {address}
"
                f"🐦 Twitter: {twitter}
"
                f"📢 Telegram: {telegram_link}"
            )
            try:
                bot.send_message(chat_id=CHAT_ID, text=message)
                sent_tokens.add(address)
            except Exception as e:
                print(f"Erro ao enviar mensagem: {e}")

    time.sleep(30)
