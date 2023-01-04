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
