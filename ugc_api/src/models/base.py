from uuid import UUID, uuid4

import orjson
from pydantic import BaseModel as PydanticModel
from pydantic import Field


def orjson_dumps(v, *, default):
    return orjson.dumps(v, default=default).decode()


class OrjsonMixin(PydanticModel):

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps
        allow_population_by_field_name = True
        arbitrary_types_allowed = True


class BaseModel(OrjsonMixin):
    id: UUID = Field(alias='_id', default_factory=uuid4)
