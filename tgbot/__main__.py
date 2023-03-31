import logging

from telegram.ext import CommandHandler, Updater

from config import config
from tgbot.api import api

logger = logging.getLogger(__name__)

logging.basicConfig(level=logging.INFO)


def user_registration(update, context):
    logger.info('Вызван /start')

    user = update.effective_user
    username = user.username
    tgid = user.id
    first_name = user.first_name
    last_name = user.last_name
    chat_id = update.message.chat_id
    context.bot.send_message(
                    chat_id=update.message.chat_id,
                    text=f'Привет {username}!\n'
                    f'Имя: {first_name} {last_name}\n'
                    f'Твой id: {tgid}\n'
                    f'id чата: {chat_id}'
                )
    api.users.registrate(username=username, tgid=tgid)


def main():

    mybot = Updater(config.api_key, use_context=True)
    dp = mybot.dispatcher
    dp.add_handler(CommandHandler('start', user_registration))
    logging.info('Бот Стартовал')
    mybot.start_polling()
    mybot.idle()


if __name__ == "__main__":
    main()
