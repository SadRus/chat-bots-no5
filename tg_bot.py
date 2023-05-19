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
from elastic_handlers import get_access_token
from state_handlers import (
    start,
    button,
    description_button,
    cart_button,
    handle_email,
)


_database = None


def handle_users_reply(update, context):
    db = get_database_connection()
    client_id = os.getenv('ELASTIC_CLIENT_ID')
    client_secret = os.getenv('ELASTIC_CLIENT_SECRET')
    elastic_token = get_access_token(client_id, client_secret)

    if update.message:
        user_reply = update.message.text
        chat_id = update.message.chat_id
    elif update.callback_query:
        user_reply = update.callback_query.data
        chat_id = update.callback_query.message.chat_id
    else:
        return None

    if user_reply == '/start':
        user_state = 'START'
    else:
        user_state = db.get(chat_id)

    states_functions = {
        'START': start,
        'HANDLE_MENU': button,
        'HANDLE_DESCRIPTION': description_button,
        'HANDLE_CART': cart_button,
        'WAITING_EMAIL': handle_email,
    }
    state_handler = states_functions[user_state]
    try:
        next_state = state_handler(
            update,
            context,
            elastic_token=elastic_token,
        )
        db.set(chat_id, next_state)
    except Exception as err:
        print(err)


def get_database_connection():
    global _database
    if _database is None:
        database_host = os.getenv("REDIS_HOST")
        database_port = os.getenv("REDIS_PORT")
        _database = redis.Redis(
            host=database_host,
            port=database_port,
            decode_responses=True,
        )
    return _database


def main():
    load_dotenv()

    tg_token = os.getenv('TG_BOT_TOKEN')

    updater = Updater(tg_token)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CallbackQueryHandler(handle_users_reply))
    dispatcher.add_handler(MessageHandler(Filters.text, handle_users_reply))
    dispatcher.add_handler(CommandHandler('start', handle_users_reply))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
