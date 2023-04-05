import pytest

from tgbot.errors import IncorrectAddCmdError
from tgbot.products import parse_add_product_cmd


@pytest.mark.parametrize('cmd, exp_category, exp_product', [
    ('/add Учебник - Книга по Python', 'Учебник', 'Книга по Python'),
    ('/add Фильм - Интерстеллар', 'Фильм', 'Интерстеллар'),
    ('/add Плюшевый динозавр - Тирекс', 'Плюшевый динозавр', 'Тирекс'),
    ('/add Мороженное - Фисташка-с-клубник', 'Мороженное', 'Фисташка-с-клубник'),
])
def test_parsed(cmd, exp_category, exp_product):
    category, product = parse_add_product_cmd(cmd)
    assert category == exp_category
    assert product == exp_product


@pytest.mark.parametrize('cmd', [
    '/add Книга',
    '/add',
])
def test_empty_product(cmd):
    with pytest.raises(IncorrectAddCmdError):
        parse_add_product_cmd(cmd)
