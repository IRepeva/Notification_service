from http import HTTPStatus

import pika
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from db.postgres import get_db
from db.rabbit import get_rabbit
from models import schemas
from services.templates import TemplateService
from services import publisher
from services.publisher import get_queue

router = APIRouter()


@router.post("/", summary="Create a notification")
async def create_notification(
        event: schemas.Event,
        session: AsyncSession = Depends(get_db),
        connection: pika.BlockingConnection = Depends(get_rabbit)
):
    """
    Create a notification with all the information:

    - **users**: list of users' ids to whom send a notification
    - **event**: event to notification
    - **data**: additional data for notification
    """
    template = await TemplateService.get_template_by_event(
        session, event=event.event
    )
    if not template:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f"Template for event {event} not found"
        )
    notification = schemas.Notification(
        **event.dict(),
        template=template.text,
        subject=template.title
    )
    publisher.publish(
        message=notification.json(),
        connection=connection,
        queue=get_queue(template.is_instant)
    )
    return HTTPStatus.OK
