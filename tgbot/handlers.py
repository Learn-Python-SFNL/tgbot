import logging

from tgbot.api import api
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
