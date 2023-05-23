import logging
import os
import redis
import time

from dotenv import load_dotenv
import telegram
from telegram.ext import (
    CallbackQueryHandler,
    CommandHandler,
    Filters,
    MessageHandler,
    Updater,
)

from create_argparser import create_parser
from elastic_handlers import get_access_token
from state_handlers import (
    start,
    handle_menu_button,
    handle_description_button,
    handle_cart_button,
    handle_email,
)
from tg_handlers import TelegramLogsHandler


logger = logging.getLogger('tg_bot_no5_logger')
_database = None


def handle_users_reply(update, context):
    db = get_database_connection()
    client_id = os.getenv('ELASTIC_CLIENT_ID')
    client_secret = os.getenv('ELASTIC_CLIENT_SECRET')

    timestamp = time.time()
    token_expiration_timestamp = context.user_data.get(
        'token_expiration_timestamp', timestamp
    )
    elastic_token = context.user_data.get('elastic_token', None)
    if timestamp > token_expiration_timestamp or elastic_token is None:
        elastic_token_content = get_access_token(client_id, client_secret)
        elastic_token = elastic_token_content['access_token']
        context.user_data['elastic_token'] = elastic_token
        context.user_data['token_expiration_timestamp'] = elastic_token_content['expires']

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
        'HANDLE_MENU': handle_menu_button,
        'HANDLE_DESCRIPTION': handle_description_button,
        'HANDLE_CART': handle_cart_button,
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
    parser = create_parser()
    args = parser.parse_args()

    tg_token = os.getenv('TG_BOT_TOKEN')
    tg_bot_logger_token = os.getenv('TG_BOT_LOGGER_TOKEN')
    tg_log_chat_id = os.getenv('TG_CHAT_ID')

    tg_bot_logger = telegram.Bot(token=tg_bot_logger_token)
    logs_full_path = os.path.join(args.dest_folder, 'tg_bot_no5.log')
    os.makedirs(args.dest_folder, exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        filename=logs_full_path,
        filemode='w',
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    )
    logger.setLevel(logging.INFO)
    handler = TelegramLogsHandler(
        logs_full_path,
        tg_bot=tg_bot_logger,
        chat_id=tg_log_chat_id,
        maxBytes=args.max_bytes,
        backupCount=args.backup_count,
    )
    logger.addHandler(handler)

    updater = Updater(tg_token)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CallbackQueryHandler(handle_users_reply))
    dispatcher.add_handler(MessageHandler(Filters.text, handle_users_reply))
    dispatcher.add_handler(CommandHandler('start', handle_users_reply))

    try:
        updater.start_polling()
        logger.info('Telegram chat-bot #5 @FishkaDevShopbot started')
    except Exception as e:
        logger.exception(e)


if __name__ == '__main__':
    main()
