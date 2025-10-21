# bot.py
import os
import sqlite3
from telebot import TeleBot, types
from dotenv import load_dotenv
import re

from generate import generate_sentence, load_model

load_dotenv()
bot = TeleBot(os.getenv("BOT_TOKEN"))
db_path = os.getenv("DB_PATH")

bot.set_my_commands([
    types.BotCommand("start", "Start the bot and choose an n-gram"),
    types.BotCommand("help", "Show usage information"),
])

pending_messages = {}

# --- SQLite setup ---
conn = sqlite3.connect(db_path, check_same_thread=False)
c = conn.cursor()
c.execute("""CREATE TABLE IF NOT EXISTS ratings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    message TEXT NOT NULL,
    rating INTEGER NOT NULL
)""")
conn.commit()
# ---------------------


# --- Loading the models ---
min_len = 10
max_len = 15

model_1, _ = load_model(os.path.join("models", "chat_1_gram.pkl"))
model_2, _ = load_model(os.path.join("models", "chat_2_gram.pkl"))
model_3, _ = load_model(os.path.join("models", "chat_3_gram.pkl"))
model_4, _ = load_model(os.path.join("models", "chat_4_gram.pkl"))
# --------------------------


def escape_markdown(text: str, version: int = 2) -> str:
    """
    Escapes Telegram MarkdownV2 special characters.
    """
    escape_chars = r'_*[]()~`>#+-=|{}.!'
    return re.sub(f'([{re.escape(escape_chars)}])', r'\\\1', text)


@bot.message_handler(commands=['help'])
def send_welcome(msg):
    bot.reply_to(msg, "I’m a simple bigram bot.\nMore info: https://github.com/LessVegetables/BiGram\nClick \\start")


@bot.message_handler(commands=['start'])
def buttons(msg):
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.row("1-gram", "Bigram")
    kb.row("3-gram", "4-gram")
    bot.send_message(msg.chat.id, "What would you like me to generate:", reply_markup=kb)


@bot.message_handler(func=lambda m: True)
def echo_all(msg):
    if msg.text == "1-gram":
        generated_text = generate_sentence(model_1, 1, min_len, max_sentence_len=max_len)
    elif msg.text == "Bigram":
        generated_text = generate_sentence(model_2, 2, min_len, max_sentence_len=max_len)
    elif msg.text == "3-gram":
        generated_text = generate_sentence(model_3, 3, min_len, max_sentence_len=max_len)
    elif msg.text == "4-gram":
        generated_text = generate_sentence(model_4, 4, min_len, max_sentence_len=max_len)
    else:
        bot.reply_to(msg, f"I don't have that one yet :(")
        return
    
    safe_text = escape_markdown(generated_text, version=2)
    message = safe_text + "\n\n_How did I do?_\n_1 — gibberish_\n_5 — perfect sentence_"

    # Inline buttons for rating
    markup = types.InlineKeyboardMarkup()
    buttons = [types.InlineKeyboardButton(str(i), callback_data=f"rate:{i}") for i in range(1, 6)]
    markup.row(*buttons)

    sent_msg = bot.send_message(msg.chat.id, message, reply_markup=markup, parse_mode="MarkdownV2")
    
    # Store the text for later reference
    if len(pending_messages) >= 100:
        # remove the first inserted key (oldest)
        oldest_key = next(iter(pending_messages))
        pending_messages.pop(oldest_key)
    pending_messages[sent_msg.message_id] = generated_text


@bot.callback_query_handler(func=lambda call: call.data.startswith("rate:"))
def handle_rating(call):
    try:
        rating = int(call.data.split(":")[1])
    except (IndexError, ValueError):
        bot.answer_callback_query(call.id, "Invalid rating data.")
        return

    msg_id = call.message.message_id
    text = pending_messages.get(msg_id)

    # Handle missing message safely
    if not text:
        bot.answer_callback_query(call.id, "This message has expired or was already rated.")
        return

    # Save to SQLite
    try:
        c.execute("INSERT INTO ratings (message, rating) VALUES (?, ?)", (text, rating))
        conn.commit()
    except Exception as e:
        print("DB error:", e)
        bot.answer_callback_query(call.id, "Database error.")
        return

    # Edit the message to show rating
    updated_text = f"{text}\n\n✅ Rated: {rating}/5"
    try:
        bot.edit_message_text(updated_text, call.message.chat.id, msg_id)
    except Exception as e:
        print("Edit error:", e)
        # Just continue — the bot shouldn’t crash if edit fails

    # Clean up safely
    pending_messages.pop(msg_id, None)

    bot.answer_callback_query(call.id, f"You rated {rating}/5. Thanks!")

if __name__ == "__main__":
    # Long polling (simple for local/dev)
    bot.infinity_polling(skip_pending=True)
