import logging

import httpx
from telegram.ext import CommandHandler, Updater

from config import config
from tgbot.api import api

logger = logging.getLogger(__name__)

logging.basicConfig(level=logging.INFO)


def get_categories():
    response = httpx.get('http://127.0.0.1:8000/api/v1/categories/')
    response.raise_for_status()
    return response.json()


def post_product(uid, product):
    products = {
        'category_id': uid,
        'title': product,
    }
    response = httpx.post('http://127.0.0.1:8000/api/v1/products/', json=products)
    response.raise_for_status()
    return response.json()


def user_registration(update, context):
    logger.info('Вызван /start')

    user = update.effective_user
    username = user.username
    tgid = user.id
    first_name = user.first_name
    context.bot.send_message(
        chat_id=update.message.chat_id,
        text=f'Привет {first_name}! Это проект Swap4newlife.\n'
        f'Я создан для того, чтобы подарить вещам вторую жизнь.\n'
        f'Если у тебя накопилось много ненужных вещей, '
        f'я помогу тебе обменять их на нужные!'
    )
    api.users.registrate(username=username, tgid=tgid)


def add_product(update, context):
    categories = get_categories()
    title = categories['title']


def choose_categoties(update, context):
    if context.args:
        message = 'Поздравляю, вы выбрали категорию!'
    else:
        message = 'Такой категории нет'
    update.message.reply_text(message)


def main():

    mybot = Updater(config.api_key, use_context=True)
    dp = mybot.dispatcher  # type: ignore
    dp.add_handler(CommandHandler('start', user_registration))
    logging.info('Бот Стартовал')
    mybot.start_polling()
    mybot.idle()


if __name__ == '__main__':
    main()
