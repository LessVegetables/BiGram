# bot.py
import os
from telebot import TeleBot, types
from dotenv import load_dotenv

from generate import generate_sentence, load_model

load_dotenv()
bot = TeleBot(os.getenv("BOT_TOKEN"))

# --- Loading the models ---
num_lines = 5
min_len = 10
max_len = 15

model_1, _ = load_model(os.path.join("models", "chat_1_gram.pkl"))
model_2, _ = load_model(os.path.join("models", "chat_2_gram.pkl"))
model_3, _ = load_model(os.path.join("models", "chat_3_gram.pkl"))
model_4, _ = load_model(os.path.join("models", "chat_4_gram.pkl"))
# --------------------------

@bot.message_handler(commands=['help'])
def send_welcome(msg):
    bot.reply_to(msg, "I’m a simple bigram bot.\nMore info: https://github.com/LessVegetables/BiGram\nWhat would you like me to generate?")

@bot.message_handler(commands=['start'])
def buttons(msg):
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.row("1-gram", "Bigram")
    kb.row("3-gram", "4-gram")
    bot.send_message(msg.chat.id, "What would you like me to generate:", reply_markup=kb)

@bot.message_handler(func=lambda m: True)
def echo_all(msg):
    if msg.text == "1-gram":
        message = generate_sentence(model_1, 1, min_len, max_sentence_len=max_len)
    elif msg.text == "Bigram":
        message = generate_sentence(model_2, 2, min_len, max_sentence_len=max_len)
    elif msg.text == "3-gram":
        message = generate_sentence(model_3, 3, min_len, max_sentence_len=max_len)
    elif msg.text == "4-gram":
        message = generate_sentence(model_4, 4, min_len, max_sentence_len=max_len)
    else:
        bot.reply_to(msg, f"I don't have that one yet :(")
    
    bot.send_message(msg.chat.id, message)

if __name__ == "__main__":
    # Long polling (simple for local/dev)
    bot.infinity_polling(skip_pending=True)
