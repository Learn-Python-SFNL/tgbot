import logging
import re

from tgbot.api import api
from tgbot.errors import IncorrectAddCmdError
from tgbot.products import parse_add_product_cmd
from tgbot.render import (
    great_user,
    noname_category,
    show_add_product,
    show_categories,
    show_choose_product,
    show_handlers,
    show_want_handler_reply,
)

logger = logging.getLogger(__name__)

choose_cmd_re = re.compile(r'\/choose (\d*).*')


def user_registration(update, context):
    logger.info('Вызван /start')

    user = update.effective_user
    api.users.registrate(username=user.username, tgid=user.id)

    great_msg = great_user(user)
    update.message.reply_text(great_msg)

    categories = api.categories.get_categories()
    categories_msg = show_categories(categories)
    update.message.reply_text(categories_msg)

    handler_msg = show_handlers()
    update.message.reply_text(handler_msg)


def add_product(update, context):
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

    chooses = dict(enumerate(products, start=1))
    context.user_data['chooses'] = chooses

    message = show_want_handler_reply(categories[0], products)
    update.message.reply_text(message)


def choose_product(update, context):
    cmd: str = update.message.text
    logger.info('Вызванна команда %s', cmd)

    choose_groups = choose_cmd_re.match(cmd)
    if not choose_groups:
        update.message.reply_text('Введи команду /choose 1')
        return

    choose_num = int(choose_groups.groups(0)[0])
    chooses = context.user_data.get('chooses')

    user = get_user(update, context)
    user_products = api.users.get_products_by_user(user['id'])
    source_product = user_products[0]
    if not source_product:
        update.message.reply_text('Сначала добавьте свой продукт')
        return

    target_product = chooses.get(choose_num)
    if not target_product:
        update.message.reply_text('Продукт не найден')
        return

    target_product_name = target_product.get('title')
    source_product_name = source_product.get('title')

    api.chooses.choose_products(
        source_product_id=source_product['id'],
        target_product_id=target_product['id'],
    )

    msg = show_choose_product(target_product_name, source_product_name)
    update.message.reply_text(msg)


def get_user(update, context):
    user = context.user_data.get('user')
    if not user:
        user = api.users.get_by_tgid(tgid=update.effective_user.id)
        context.user_data['user'] = user

    return user
