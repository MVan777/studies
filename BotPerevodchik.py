from telebot import types, TeleBot
from yandex_gpt1 import YandexGPT
from TgDb import TelegramDB

TOKEN = ""

bot = TeleBot(TOKEN)
yandex = YandexGPT()
db = TelegramDB('tg.json')

# Кнопки задаю названия и call_back для дальнейшего использования и сравнения
def get_lang_markup():
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('Английский', callback_data='lang_en'))
    markup.add(types.InlineKeyboardButton('Французский', callback_data='lang_fr'))
    markup.add(types.InlineKeyboardButton('Поиск информации', callback_data='lang_info'))
    return markup

# При получение команды /start запускаю кнопки функцию get_lang_markup()
@bot.message_handler(commands=['start'])
def send_welcome(message):
    chat_id = message.chat.id # Получаю ИД что-бы ответным сообщением суметь ответить тому же ИД
    bot.send_message(chat_id, 'Выбери язык для перевода либо введи запрос:', reply_markup=get_lang_markup())

# Обрабатываю нажатия кнопок
@bot.callback_query_handler(func=lambda call: call.data.startswith('lang_'))
def callback_lang(call):
    chat_id = call.message.chat.id
    if call.data == 'lang_en':
        db.set_value(chat_id, "lang", "en") # Устанавливаю либо получаю "Статус"
        bot.send_message(chat_id, "Введите текст, который нужно перевести на английский:")
    elif call.data == 'lang_fr':
        db.set_value(chat_id, "lang", "fr")
        bot.send_message(chat_id, "Введите текст, который нужно перевести на французский:")
    elif call.data == 'lang_info':
        db.set_value(chat_id, "lang", "info")
        bot.send_message(chat_id, "Введите текст, для запрос или поиска:")

# Обработка текста от пользователя
@bot.message_handler(func=lambda msg: True)
def translate_text(message):
    chat_id = message.chat.id # Получаю ИД
    lang = db.get_value(chat_id, "lang") # Проверяю статус языка который выбран

    # Ели язык не выбран запускаю меню для выбора
    if not lang:
        bot.send_message(chat_id, "Сначала выбери язык через /start", reply_markup=get_lang_markup())
        return

    # Получаю текст для перевода и записываю в промт с условиями для выбора языка
    text_to_translate = message.text
    if lang == "en":
        prompt = f"Переведи на английский: {text_to_translate}"
    elif lang == "fr":
        prompt = f"Переведи на французский: {text_to_translate}"
    elif lang == "info":
        prompt = f"Найди запрос от пользователя или ответь на вопрос: {text_to_translate}"
    else:
        bot.send_message(chat_id, "Ошибка: язык не выбран")
        return

    # Запрос к YandexGPT
    translation = yandex.get_answer([{"role": "user", "text": prompt}])

    markup_inline = types.InlineKeyboardMarkup()
    markup_inline.add(types.InlineKeyboardButton("🌐 Сменить язык", callback_data="change_lang"))

    # После получения ответа от яндекс передаем его на ТГ
    bot.send_message(chat_id, translation, reply_markup=markup_inline)

# Обработка кнопки смены языка
@bot.callback_query_handler(func=lambda call: call.data == 'change_lang')
def change_lang(call):
    chat_id = call.message.chat.id # Получаю ИД
    db.set_value(chat_id, "lang", None)  # Сбрасываем язык

    # После завершения цикла запускаю меню по новой
    bot.send_message(chat_id, 'Привет! Выбери язык для перевода:', reply_markup=get_lang_markup())

if __name__ == "__main__":
    bot.infinity_polling()
