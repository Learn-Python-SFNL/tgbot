from typing import Any

from jinja2 import Environment, PackageLoader, select_autoescape

jenv = Environment(
    loader=PackageLoader('tgbot'),
    autoescape=select_autoescape(),
)


def great_user(user):
    first_name = user.first_name
    template = jenv.get_template('reg.j2')
    return template.render(first_name=first_name)


def show_categories(categories):
    template = jenv.get_template('all_categories.j2')
    return template.render(categories=categories)


def show_add_product(product: dict[str, Any], category: dict[str, Any]):
    template = jenv.get_template('add_product.j2')
    return template.render(product_name=product['title'], category_name=category['title'])


def noname_category(category_name):
    template = jenv.get_template('no_category_text.j2')
    return template.render(category_name=category_name)


Json = dict[str, Any]


def show_want_handler_reply(category: Json, products: list[Json]):
    template = jenv.get_template('want_handler_reply.j2')
    return template.render(category=category, products=products)
