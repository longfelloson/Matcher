import uuid

from pydantic import BaseModel, UUID4, Field


class Report(BaseModel):
    report_id: UUID4 = Field(default=uuid.uuid4())
    reporter: int
    reported: int
