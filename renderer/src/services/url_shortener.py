import requests
from core.configuration import settings
from requests.structures import CaseInsensitiveDict


class UrlShortener:
    def __init__(self):
        self.url = settings.shortener.endpoint
        self.token = settings.shortener.token.get_secret_value()
        self.domain = settings.shortener.domain

    def _get_headers(self):
        headers = CaseInsensitiveDict()
        headers["Accept"] = "application/json"
        headers["Authorization"] = f"Bearer {self.token}"
        headers["Content-Type"] = "application/json"
        return headers

    def _get_data(self, url):
        data = {
            "domain": self.domain,
            "long_url": url
        }
        return data

    def get_short_url(self, url):
        headers = self._get_headers()
        data = self._get_data(url)
        resp = requests.post(self.url, headers=headers, json=data)
        return resp.json()['link']

