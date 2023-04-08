import logging

from tgbot.api import api
from tgbot.errors import IncorrectAddCmdError
from tgbot.products import parse_add_product_cmd
from tgbot.render import great_user, noname_category, show_add_product, show_categories

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
        categories = api.categories.get_categories()
        update.message.reply_text(noname_category(category_name))
        categories_msg = show_categories(categories)
        update.message.reply_text(categories_msg)
        return

    user = api.users.get_by_tgid(tgid=update.effective_user.id)
    product = api.products.add(
        category_id=categories[0]['id'],
        title=product_name,
        user_id=user['id'],
    )
    product_add = show_add_product(product, categories[0])
    update.message.reply_text(product_add)
