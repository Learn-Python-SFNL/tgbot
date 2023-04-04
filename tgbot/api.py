from http import HTTPStatus

import httpx
from jinja2 import Environment, PackageLoader, select_autoescape

from config import config

jenv = Environment(
    loader=PackageLoader('tgbot'),
    autoescape=select_autoescape(),
)


# TODO: класс categories.client класс products.client
class UserClient:
    def __init__(self, url: str):
        self.url = f'{url}/api/v1/users/'

    def registrate(self, username: str, tgid: int):
        users = {'username': username, 'tgid': tgid}
        response = httpx.post(self.url, json=users)
        if response.status_code == HTTPStatus.CONFLICT:
            return False
        response.raise_for_status()
        return True

    def greet_user(self, update):
        user = update.effective_user
        username = user.username
        tgid = user.id
        first_name = user.first_name
        api.users.registrate(username=username, tgid=tgid)
        template = jenv.get_template('reg.j2')
        return template.render(first_name=first_name)


class CategoriesClient:
    def __init__(self, url: str):
        self.url = f'{url}/api/v1/categories/'

    def get_categories(self):
        response = httpx.get(self.url)
        return response.json()

    def all_categories(self):
        template2 = jenv.get_template('all_categories.j2')
        categories = api.categories.get_categories()
        return template2.render(categories=categories)


class ApiClient:
    def __init__(self, url: str):
        # self.products =
        self.categories = CategoriesClient(url=url)
        self.users = UserClient(url=url)


api = ApiClient(url=config.http_key)
