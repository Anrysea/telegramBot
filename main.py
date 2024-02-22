from telegram import Update
import openai
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Инициализация словаря
users_data = {}
users_mode = {}
to_japanese = [{"role": "user", "content": "В этом диалоге переводи все мои сообщения на японский."}]
from_japanese = [{"role": "user", "content": "В этом диалоге переводи мои сообщения с японского на русский."}]
grammar = [{"role": "user", "content": "Чат для изучения японской грамматики. Объясни все употребления."}]
openai.api_key = ""

def generate_response(message_dict):

    completion = openai.ChatCompletion.create(
        model="gpt-4",
        messages=message_dict
    )
    # Получение сгенерированного ответа из результата API
    return completion.choices[0].message.content.strip()


def start(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    # if user_id not in users_data:
    #     users_data[user_id] = []
    # users_data[user_id].append(update.message.text)

    update.message.reply_text('Здравствуй! Я твой новый бот.')

def clear(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    text = ""
    if user_id not in users_mode:
        users_mode[user_id] = 0

    users_data[user_id] = []

    if users_mode[user_id] == 0:
        text = 'Диалог обновлён, режим - Обычный'
    elif users_mode[user_id] == 1:
        users_data[user_id] = to_japanese
        text = 'Диалог обновлён, режим - Перевод на японский'
    elif users_mode[user_id] == 2:
        users_data[user_id] = from_japanese
        text = 'Диалог обновлён, режим - Перевод с японского'
    elif users_mode[user_id] == 3:
        users_data[user_id] = grammar
        text = 'Диалог обновлён, режим - Объяснение грамматики'
    # if user_id not in users_data:
    #     users_data[user_id] = []
    # users_data[user_id].append(update.message.text)

    update.message.reply_text(text)

def default(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    users_mode[user_id] = 0
    users_data[user_id] = []
    update.message.reply_text('Диалог обновлён, режим - Обычный')

def toJ(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    users_mode[user_id] = 1
    users_data[user_id] = []
    users_data[user_id] = to_japanese
    update.message.reply_text('Диалог обновлён, режим - Перевод на японский')

def fromJ(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    users_mode[user_id] = 2
    users_data[user_id] = []
    users_data[user_id] = from_japanese
    update.message.reply_text('Диалог обновлён, режим - Перевод с японского')

def gramm(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    users_mode[user_id] = 3
    users_data[user_id] = []
    users_data[user_id] = grammar
    update.message.reply_text('Диалог обновлён, режим - Объяснение грамматики')


def echo(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    if user_id not in users_data:
        users_data[user_id] = []
    message_text = update.message.text
    users_data[user_id].append({"role": "user", "content": message_text})
    result = generate_response(message_dict=users_data[user_id])
    print(user_id, message_text)
    users_data[user_id].append({"role": "assistant", "content": result})
    update.message.reply_text(result)


def main() -> None:
    updater = Updater("6432658617:AAErEp6QjL6k9mlPyuoQOd6xBzeLf427foY")

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("clear", clear))
    dispatcher.add_handler(CommandHandler("default", default))
    dispatcher.add_handler(CommandHandler("from_japanese", fromJ))
    dispatcher.add_handler(CommandHandler("to_japanese", toJ))
    dispatcher.add_handler(CommandHandler("grammar", gramm))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()