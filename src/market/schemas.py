from pydantic import BaseModel


class OffsetLimit(BaseModel):
    offset: int = 0
    limit: int = 25
    