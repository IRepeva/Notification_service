from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class TemplateIn(BaseModel):
    event: str
    is_instant: bool
    title: str
    text: str


class TemplateSchema(TemplateIn):
    id: int

    class Config:
        orm_mode = True


class Event(BaseModel):
    users: list[UUID]
    event: str
    data: dict


class Notification(Event):
    notification_id: UUID = Field(default_factory=uuid4)
    template: str
    subject: str
