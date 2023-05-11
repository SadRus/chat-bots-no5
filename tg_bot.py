import os
import redis

from dotenv import load_dotenv
from telegram.ext import (
    CallbackQueryHandler,
    CommandHandler,
    Filters,
    MessageHandler,
    Updater,
)


def start(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='Hello, squizers!\nНажмите "Новый вопрос" для начала викторины.',
    )


def main():
    load_dotenv()

    tg_token = os.getenv('TG_BOT_TOKEN')

    updater = Updater(tg_token)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
