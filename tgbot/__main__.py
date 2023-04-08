import logging

from telegram.ext import CommandHandler, Updater

from config import config
from tgbot.handlers import add_product, user_registration, want_products_reply

logger = logging.getLogger(__name__)


def main():

    logging.basicConfig(level=config.log_level)
    mybot = Updater(config.api_key, use_context=True)
    dp = mybot.dispatcher  # type: ignore
    dp.add_handler(CommandHandler('start', user_registration))
    dp.add_handler(CommandHandler('add', add_product))
    dp.add_handler(CommandHandler('want', want_products_reply))
    logging.info('Бот Стартовал')
    mybot.start_polling()
    mybot.idle()


if __name__ == '__main__':
    main()
