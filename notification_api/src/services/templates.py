from models import models, schemas
from models.models import Template
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select


class TemplateService:
    @classmethod
    async def get_template_by_event(cls, session: AsyncSession, event: str):
        result = await session.execute(
            select(Template).where(Template.event == event)
        )
        return result.scalars().first()

    @classmethod
    async def create_template(
            cls,
            session: AsyncSession,
            template: schemas.TemplateIn
    ) -> Template:
        new_template = models.Template(**template.dict())
        return await cls.save_template(session, new_template)

    @classmethod
    async def edit_template(
            cls,
            session: AsyncSession,
            template: schemas.TemplateIn,
            event: str
    ) -> Template:
        db_template = await cls.get_template_by_event(session, event)
        db_template.title = template.title
        db_template.text = template.text
        db_template.is_instant = template.is_instant
        return await cls.save_template(session, db_template)

    @classmethod
    async def save_template(cls, session: AsyncSession, template: Template):
        session.add(template)
        await session.commit()
        await session.refresh(template)
        return template
