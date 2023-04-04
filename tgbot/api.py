from http import HTTPStatus

import httpx

from config import config


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


class CategoriesClient:
    def __init__(self, url: str):
        self.url = f'{url}/api/v1/categories/'

    def get_categories(self):
        response = httpx.get(self.url)
        return response.json()


class ApiClient:
    def __init__(self, url: str):
        # self.products =
        self.categories = CategoriesClient(url=url)
        self.users = UserClient(url=url)


api = ApiClient(url=config.http_key)
