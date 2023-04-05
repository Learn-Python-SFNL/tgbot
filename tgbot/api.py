from http import HTTPStatus

import httpx
from typing import Any
from config import config


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

    def get_categories_by_name(self, name: str):
        response = httpx.get(self.url, params={'title': name})
        return response.json()


class ProductsClient:
    def __init__(self, url: str):
        self.url = f'{url}/api/v1/products/'

    def add(self, category_id: int, title: str) -> dict[str, Any]:
        payload = {
            'category_id': category_id,
            'title': title,
        }
        response = httpx.post(self.url, json=payload)
        return response.json()


class ApiClient:
    def __init__(self, url: str):
        self.products = ProductsClient(url=url)
        self.categories = CategoriesClient(url=url)
        self.users = UserClient(url=url)


api = ApiClient(url=config.http_key)
