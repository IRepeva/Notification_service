import logging
from abc import ABC, abstractmethod

from jinja2 import BaseLoader, Environment
from jinja2.exceptions import TemplateSyntaxError

logger = logging.getLogger()


class TemplateRenderer(ABC):
    @abstractmethod
    def template_render(self, template: str, data: dict) -> str:
        ...


class JanjaTemplateRenderer(TemplateRenderer):

    def __init__(self) -> None:
        self.env = Environment(loader=BaseLoader)

    def template_render(self, template: str, data: dict) -> str:
        template = self.env.from_string(template)
        try:
            letter = template.render(**data)
        except TemplateSyntaxError:
            logger.exception('Template syntax error %s.', template)
            raise TemplateSyntaxError
        return letter
