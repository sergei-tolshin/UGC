from uuid import UUID, uuid4

import orjson
from bson import ObjectId
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


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError('Invalid object id')
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type='string')


class CreateResponseModel(OrjsonMixin):
    inserted_id: str
    acknowledged: bool
