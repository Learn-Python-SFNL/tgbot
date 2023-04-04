import logging

import httpx
from telegram.ext import CommandHandler, Updater

from config import config
from tgbot.errors import IncorrectAddCmdError
from tgbot.handlers import user_registration
from tgbot.products import parse_add_product_cmd

logger = logging.getLogger(__name__)

logging.basicConfig(level=logging.INFO)


# TODO: переместить в api.py в категориес клиента


def get_categories():
    response = httpx.get('http://127.0.0.1:8000/api/v1/categories/')
    response.raise_for_status()
    return response.json()


# TODO: переместить в api.py в продуктс клиента
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


def get_categories_by_name(name: str):
    response = httpx.get('http://127.0.0.1:8000/api/v1/categories/', params={'title': name})
    logger.info(response.status_code)
    logger.info(response.text)
    return response.json()


def add_product(update, context):
    """/add Учебник - Книга по Python."""
    try:
        category_name, product_name = parse_add_product_cmd(update.message.text)
    except IncorrectAddCmdError as err:
        update.message.reply_text(err.message, parse_mode='MarkdownV2')

    # TODO: categories = api.caterories.get_by_name(category_name)
    # Проверить что категория одна, если их нет дать один ответ  и если несколько - другой
    # Если одна, api.products.add(categories[0]['id'], product_title)
    # Сказать пользователю, что продукт добавлен
    categories = api.caterories.get_categories_by_name(category_name)

    if not categories:
        update.message.reply_text(f'Категории "{category_name}" нет')
        update.message.reply_text(f'Вот список категорий: {names} выберите нужную')
    else:
        post = api.products.add(categories[0]['id'], product_title)
        update.message.reply_text(f'Вы успешно добавили продукт {product_name} в категории {category_name}')


def main():

    mybot = Updater(config.api_key, use_context=True)
    dp = mybot.dispatcher  # type: ignore
    dp.add_handler(CommandHandler('start', user_registration))
    dp.add_handler(CommandHandler('add', add_product))
    logging.info('Бот Стартовал')
    mybot.start_polling()
    mybot.idle()


if __name__ == '__main__':
    main()
