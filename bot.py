from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from transformers import pipeline
import os
from dotenv import load_dotenv
load_dotenv()


TELEGRAM_API_TOKEN = os.getenv("TELEGRAM_API_TOKEN")

if TELEGRAM_API_TOKEN is None:
    raise ValueError("API-Token not found! Please check the .env-file.")

pipe = pipeline(model="TinyLlama/TinyLlama-1.1B-Chat-v1.0")

def generate_response(user_input):
    prompt = f"You are an AI assistant. Your task is to provide relevant and helpful information based on the user's question.\nUser: {user_input}\nAI:"

    # Generiere eine Antwort mit dem angegebenen Prompt
    result = pipe(prompt, max_length=250, num_return_sequences=1, do_sample=True, temperature=0.7)

    # Extrahiere die Antwort ohne den Prompt-Text
    response = result[0]["generated_text"]

    # Entferne den ursprünglichen Prompt-Text aus der Antwort
    return response.split("AI:")[-1].strip()

def start(update: Update, context: CallbackContext):
    update.message.reply_text("Hi! I am an AI assistant. How can I help you today?")

def process(update: Update, context: CallbackContext):
    user_message = update.message.text
    response = generate_response(user_message)  # Nachricht an das Modell
    update.message.reply_text(response)

def main():
    updater = Updater(TELEGRAM_API_TOKEN, use_context=True)

    # Dispatcher für Befehle und Nachrichten
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, process))

    # Bot starten
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()


