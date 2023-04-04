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
