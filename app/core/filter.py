from typing import Literal
from pydantic import BaseModel, Field


class Filter(BaseModel):
    """
    Base class for filters.
    """

    limit: int = Field(10, ge=1, le=100)
    offset: int = Field(0, ge=0)
    order_by: Literal["id"] = "id"
