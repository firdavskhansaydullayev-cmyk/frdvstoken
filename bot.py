import telebot
import json
import os
from flask import Flask, request

BOT_TOKEN = os.environ.get('BOT_TOKEN', '')
WEB_APP_URL = os.environ.get('WEB_APP_URL', '')

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

DATA_FILE = 'users.json'

def load_users():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_users(users):
    with open(DATA_FILE, 'w') as f:
        json.dump(users, f)

@bot.message_handler(commands=['start'])
def start(message):
    users = load_users()
    uid = str(message.from_user.id)
    ref = message.text.split()[1] if len(message.text.split()) > 1 else None
    
    if uid not in users:
        users[uid] = {
            'name': message.from_user.first_name,
            'score': 0,
            'refs': []
        }
        if ref and ref != uid and ref in users:
            users[ref]['score'] += 1000
            users[ref]['refs'].append(uid)
        save_users(users)
    
    markup = telebot.types.InlineKeyboardMarkup()
    btn = telebot.types.InlineKeyboardButton(
        '🪙 O\'YINNI BOSHLASH',
        web_app=telebot.types.WebAppInfo(url=WEB_APP_URL)
    )
    markup.add(btn)
    bot.send_message(message.chat.id,
        f'Salom {message.from_user.first_name}! 👋\n\n🪙 FRDVS Token o\'yiniga xush kelibsiz!\n\nHar kun token yig\'ing va do\'stlaringizni taklif qiling!',
        reply_markup=markup)

@app.route('/' + BOT_TOKEN, methods=['POST'])
def webhook():
    update = telebot.types.Update.de_json(request.data.decode('utf-8'))
    bot.process_new_updates([update])
    return 'ok'

@app.route('/')
def index():
    return 'Bot ishlayapti!'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
