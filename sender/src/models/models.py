import uuid

from pydantic import BaseModel


class Notification(BaseModel):
    notification_id: uuid.UUID
    user_id: uuid.UUID
    content_id: str
    type: str


class EmailTemplate(BaseModel):
    email: str
    letter: str
    subject: str
    content_id: str
    user_id: uuid.UUID
    notification_id: uuid.UUID
