import uuid

from pydantic import UUID4, Field, BaseModel


class Report(BaseModel):
    report_id: UUID4 = Field(default=uuid.uuid4())
    reporter: int
    reported: int
