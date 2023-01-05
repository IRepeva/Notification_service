from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from db.postgres import get_db
from models.schemas import TemplateInput, TemplateSchema
from services.templates import TemplateService

router = APIRouter()


@router.post(
    "/create",
    response_model=TemplateSchema,
    summary="Create a template"
)
async def create_template(
        new_template: TemplateInput,
        session: AsyncSession = Depends(get_db)
):
    """
    Create a template for the event:

    - **event**: notification event
    - **is_instant**: instant notification or not
    - **title**: subject of notification
    - **text**: template of notification
    """
    template = await TemplateService.get_template_by_event(
        session, event=new_template.event
    )
    if template:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=f"Template for the event {new_template.event} already exists"
        )
    return await TemplateService.create_template(
        session=session, template=new_template
    )


@router.put(
    "/{event}/edit",
    response_model=TemplateSchema,
    summary="Edit the template"
)
async def edit_template(
        event: str,
        new_template: TemplateInput,
        session: AsyncSession = Depends(get_db)
):
    """
    Change a template for the event:

    - **event**: notification event
    - **is_instant**: instant notification or not
    - **title**: subject of notification
    - **text**: template of notification
    """
    template = await TemplateService.get_template_by_event(session, event=event)
    if not template:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f"Template for event {new_template.event} not found"
        )
    return await TemplateService.edit_template(
        session=session, template=new_template, event=event
    )
