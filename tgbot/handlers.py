import logging

from tgbot.api import api
from tgbot.errors import IncorrectAddCmdError
from tgbot.products import parse_add_product_cmd
from tgbot.render import (
    great_user,
    noname_category,
    show_add_product,
    show_categories,
    show_want_handler_reply,
    show_choose_product,
)

logger = logging.getLogger(__name__)


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


def want_products_reply(update, context):
    """Вернуть список продуктов по категории Учебник.

    /want Учебник

    Книга по Python
    Книга по цветочкам
    Зельеваренье
    """
    cmd: str = update.message.text
    logger.info('Вызванна команда %s', cmd)
    category_name = ' '.join(cmd.split(' ')[1:])
    categories = api.categories.get_categories_by_name(category_name)
    if not categories:
        update.message.reply_text('Извините, такой категории нет, Вика еще учится')
        return

    # TODO: обработать случай с несколькими категориями
    category = categories[0]
    products = api.categories.get_products(category['id'])

    message = show_want_handler_reply(categories[0], products)
    update.message.reply_text(message)


def choose_product(update, context):
    choose_list = {
        1: {'id': 1, 'title': 'лучшая книга по пайтону'},
        2: {'id': 2, 'title': 'книга физика 11 класс'},
    }

    source_product_id = 1
    source_product = choose_list.get(source_product_id)
    if not source_product:
        update.message.reply_text('Продукт не найден')
        return

    target_product_id = 2
    target_product = choose_list.get(target_product_id)
    if not target_product:
        update.message.reply_text('Продукт не найден')
        return

    target_product_name = target_product.get('title')
    source_product_name = source_product.get('title')
    msg = show_choose_product(target_product_name, source_product_name)
    update.message.reply_text(msg)
