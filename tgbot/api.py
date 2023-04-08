from http import HTTPStatus
from typing import Any

import httpx

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

    def get_by_tgid(self, tgid: int):
        response = httpx.get(f'{self.url}telegram/{tgid}')
        response.raise_for_status()
        return response.json()


class CategoriesClient:
    def __init__(self, url: str):
        self.url = f'{url}/api/v1/categories/'

    def get_categories(self) -> list[dict[str, Any]]:
        response = httpx.get(self.url)
        response.raise_for_status()
        return response.json()

    def get_categories_by_name(self, name: str) -> list[dict[str, Any]]:
        response = httpx.get(self.url, params={'title': name})
        response.raise_for_status()
        return response.json()

    def get_products(self, category_id: int) -> list[dict[str, Any]]:
        response = httpx.get(f'{self.url}{category_id}/products/')
        response.raise_for_status()
        return response.json()


class ProductsClient:
    def __init__(self, url: str):
        self.url = f'{url}/api/v1/products/'

    def add(self, category_id: int, title: str, user_id: int) -> dict[str, Any]:
        payload = {
            'category_id': category_id,
            'title': title,
            'user_id': user_id,
        }
        response = httpx.post(self.url, json=payload)
        response.raise_for_status()
        return response.json()


class ApiClient:
    def __init__(self, url: str):
        self.products = ProductsClient(url=url)
        self.categories = CategoriesClient(url=url)
        self.users = UserClient(url=url)


api = ApiClient(url=config.http_key)
