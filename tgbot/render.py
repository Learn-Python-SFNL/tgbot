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
    template2 = jenv.get_template('all_categories.j2')
    return template2.render(categories=categories)


def show_add_product(product: dict[str, Any], category: dict[str, Any]):
    template3 = jenv.get_template('add_product.j2')
    return template3.render(product_name=product['title'], category_name=category['title'])


def noname_category(category_name):
    template4 = jenv.get_template('no_category_text.j2')
    return template4.render(category_name=category_name)
