from abc import ABC, abstractmethod

from services.database_service import BaseDBService


class BaseSender(ABC):
    def __init__(self, database_service: BaseDBService):
        self.db_service = database_service

    @abstractmethod
    def send(self, data):
        ...
