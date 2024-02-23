import telebot
import gpt
import config
import sqlite3
import logging

bot = telebot.TeleBot(config.BOT_TOKEN)

connect = sqlite3.connect('users.db', check_same_thread=False)
cursor = connect.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS users (id INTEGER, question TEXT, answer TEXT)''')
connect.commit()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    filename="log_file.txt",
    filemode="w",
)

@bot.message_handler(commands=['start'])
def start(message):
    logging.info("Отправка приветственного сообщения")
    bot.send_message(message.chat.id, 'Привет! Я бот-помощник. Чем могу помочь?')

@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, 'Я могу отвечать на текстовые вопросы. Просто отправь мне свой вопрос.')

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        question = message.text
        logging.debug(f"Полученный текст от пользователя: {message.text}")
        response = gpt.generate_response(question)
        cursor.execute(f"INSERT INTO users (id, question, answer) VALUES ({message.chat.id}, ?, ?)", (message.text, response))
        logging.info("Данные добавлены  в БД")
        connect.commit()
        bot.send_message(message.chat.id, response)
        logging.info("Сообщение успешно отправлено")
    except sqlite3.Error as error:
        bot.send_message(message.chat.id, "Ошибка, связанная с БД.")

if __name__ == '__main__':
    logging.info("Бот запущен")
    bot.polling()
