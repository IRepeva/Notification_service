from uuid import UUID, uuid4

from models.mixin import MixinModel
from pydantic import Field, BaseModel


class TemplateInput(MixinModel):
    event: str
    is_instant: bool
    title: str
    text: str


class TemplateSchema(BaseModel):
    id: int
    event: str
    is_instant: bool
    title: str
    text: str

    class Config:
        orm_mode = True


class Event(MixinModel):
    users: list[UUID]
    event: str
    data: dict


class Notification(Event):
    notification_id: UUID = Field(default_factory=uuid4)
    template: str
    subject: str
