import httpx

from config import config_api

# TODO: класс categories.client класс products.client
class UserClient:
    def __init__(self, url: str):
        self.url = f'{url}/api/v1/users/'

    def registrate(self, username: str, tgid: int) -> None:

        users = {'username': username, 'tgid': tgid}
        response = httpx.post(self.url, json=users)
        response.raise_for_status()


class ApiClient:
    def __init__(self, url: str):
        # self.products =
        # self.categories =
        self.users = UserClient(url=url)


api = ApiClient(url=config_api.http_key)
