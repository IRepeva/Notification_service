import orjson

from pydantic import BaseModel


def orjson_dumps(val, *, default):
    return orjson.dumps(val, default=default).decode()


class MixinModel(BaseModel):
    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps
