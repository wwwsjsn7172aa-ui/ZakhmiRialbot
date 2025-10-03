import requests
import time
import telebot

# توکن رباتت رو اینجا بذار
BOT_TOKEN = '7998734835:AAFn_DgaRGbBURcL5SQt3gco5eQ7DuSjwsQ'
OWNER_ID = 'YOUR_TELEGRAM_ID'  # آیدی عددی تلگرام تو

bot = telebot.TeleBot(BOT_TOKEN)

def fetch_tokens():
    url = 'https://api.dexscreener.com/latest/dex/pairs/solana'
    response = requests.get(url)
    data = response.json()
    return data['pairs']

def filter_token(token):
    try:
        volume = float(token['volume']['h1'])
        liquidity = float(token['liquidity']['usd'])
        tx_count = int(token['txCount']['h1'])
        holders = int(token.get('holders', 0))
        age_minutes = int(token.get('ageMinutes', 999))
        name = token['baseToken']['name'].lower()
        symbol = token['baseToken']['symbol'].lower()

        # فیلترهای پامپ
        if volume > 10000 and liquidity > 15000 and tx_count > 50 and age_minutes < 60 and holders < 300:
            if any(keyword in name for keyword in ['zakhmi', 'ashk', 'hope', 'rial']) or any(keyword in symbol for keyword in ['zrb', 'ashk', 'hope']):
                return True
    except:
        return False
    return False

def send_signal(token):
    name = token['baseToken']['name']
    address = token['pairAddress']
    volume = token['volume']['h1']
    liquidity = token['liquidity']['usd']
    link = f"https://dexscreener.com/solana/{address}"

    message = f"""
🔥 سیگنال پامپ جدید شناسایی شد!

🪙 نام: {name}
📈 حجم: {volume} دلار
🔒 نقدینگی قفل‌شده: {liquidity} دلار
🚨 امنیت: تأیید شد

📎 آدرس توکن: {address}
📎 لینک خرید: {link}

💬 پیام ربات:
"توکن زخمی، ولی امیدوار... مثل دل ما. آماده‌ی پرواز؟ 💔📈"
"""
    bot.send_message(OWNER_ID, message)

def main():
    sent = set()
    while True:
        tokens = fetch_tokens()
        for token in tokens:
            if filter_token(token):
                address = token['pairAddress']
                if address not in sent:
                    send_signal(token)
                    sent.add(address)
        time.sleep(60)

if __name__ == '__main__':
    main()