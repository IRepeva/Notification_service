from http import HTTPStatus

import requests
from utils.backoff import backoff


class UserDataExtractor:
    def __init__(self, endpoint: str, authorization: str) -> None:
        self.url = endpoint
        self.headers = {'Authorization': authorization}

    @backoff()
    def get_info(self, user_id: str) -> dict:
        response = requests.get(
            url=f"{self.url}/{user_id}",
            headers=self.headers
        )
        if response.status_code != HTTPStatus.OK:
            raise Exception(
                f"Status code {response.status_code} {response.text}"
            )
        return response.json()
