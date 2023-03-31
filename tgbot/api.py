import logging

import httpx

logger = logging.getLogger(__name__)

logging.basicConfig(level=logging.INFO)


class UserClient:
    def __init__(self, url: str):
        self.url = f'{url}/api/v1/users/'

    def registrate(self, username: str, tgid: int) -> None:

        users = {'username': username, 'tgid': tgid}
        response = httpx.post(self.url, json=users)
        response.raise_for_status()
        logger.info(response.json())


class ApiClient:
    def __init__(self, url: str):

        self.users = UserClient(url=url)


api = ApiClient(url='http://127.0.0.1:8000')
