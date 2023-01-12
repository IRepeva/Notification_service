import contextvars
import logging
import uuid

import aio_pika
import uvicorn as uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import ORJSONResponse

from api.v1 import events, templates
from core.logger import LOGGING
from core.settings import settings, Queue
from db import rabbit

_request_id = contextvars.ContextVar(
    'request_id', default=f'system:{uuid.uuid4()}'
)

app = FastAPI(
    title=settings.project_name,
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
)


@app.middleware('http')
async def request_id_middleware(request: Request, call_next):
    request_id = (
            request.headers.get('X-Request-Id')
            or f'direct:{uuid.uuid4()}'
    )
    _request_id.set(request_id)
    return await call_next(request)


factory = logging.getLogRecordFactory()


def record_factory(*args, **kwargs):
    record = factory(*args, **kwargs)
    record.request_id = _request_id.get()
    return record


app.logger = logging.getLogger(__name__)
app.logger.setLevel(logging.INFO)
logging.setLogRecordFactory(record_factory)


@app.on_event('startup')
async def startup():
    rabbit.rabbitmq = await aio_pika.connect_robust(
        host=settings.rabbit.host,
        login=settings.rabbit.user_name,
        password=settings.rabbit.password.get_secret_value()
    )
    channel = await rabbit.rabbitmq.channel()
    queue = await channel.declare_queue(Queue.instant.name, durable=True)

    channel = await rabbit.rabbitmq.channel()
    queue = await channel.declare_queue(Queue.not_instant.name, durable=True)


@app.on_event('shutdown')
async def shutdown():
    await rabbit.rabbitmq.close()


app.include_router(templates.router, prefix='/api/v1/template', tags=['template'])
app.include_router(events.router, prefix='/api/v1/event', tags=['event'])

if __name__ == '__main__':
    uvicorn.run(
        'main:src',
        host='0.0.0.0',
        port=8000,
        reload=True,
        log_config=LOGGING,
        log_level='info'
    )
