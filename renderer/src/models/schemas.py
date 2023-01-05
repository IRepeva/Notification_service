from pydantic import BaseModel


class Notification(BaseModel):
    letter: str
    content_id: str
    user_id: str
    notification_id: str


class EmailNotification(Notification):
    email: str
    subject: str
