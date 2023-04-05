import logging

from tgbot.api import api
from tgbot.errors import IncorrectAddCmdError
from tgbot.products import parse_add_product_cmd
from tgbot.render import great_user, show_categories

logger = logging.getLogger(__name__)

logging.basicConfig(level=logging.INFO)


def user_registration(update, context):
    logger.info('Вызван /start')

    user = update.effective_user
    api.users.registrate(username=user.username, tgid=user.id)

    great_msg = great_user(user)
    update.message.reply_text(great_msg)

    categories = api.categories.get_categories()
    categories_msg = show_categories(categories)
    update.message.reply_text(categories_msg)


def add_product(update, context):
    """/add Учебник - Книга по Python."""
    try:
        category_name, product_name = parse_add_product_cmd(update.message.text)
    except IncorrectAddCmdError as err:
        update.message.reply_text(err.message, parse_mode='MarkdownV2')

    categories = api.categories.get_categories_by_name(category_name)

    if not categories:
        all_categories = api.categories.get_categories()
        update.message.reply_text(f'Категории "{category_name}" нет')
        update.message.reply_text(f'Список категорий: {all_categories} выберите нужную')
    else:
        product = api.products.add(categories[0]['id'], product_name)
        update.message.reply_text(f'Вы успешно добавили продукт {product["title"]} в категории {categories[0]["title"]}')
