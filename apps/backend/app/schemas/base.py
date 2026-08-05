"""Base Schemas Module."""

from pydantic import BaseModel, ConfigDict


class BaseSchema(BaseModel):
    """Pydantic Base Schema with from_attributes enabled."""

    model_config = ConfigDict(from_attributes=True)
