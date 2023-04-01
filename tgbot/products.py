import logging

from tgbot.errors import IncorrectAddCmdError

logger = logging.getLogger(__name__)


def parse_add_product_cmd(cmd: str) -> tuple[str, str]:
    sms = cmd.split('-')
    product = '-'.join(sms[1:])
    product = product.strip()
    if not product:
        raise IncorrectAddCmdError('Продукт не заполнен')
    category_part = sms[0].split(' ')[1:]
    category = ' '.join(category_part).strip()
    return category, product
