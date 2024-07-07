from pydantic import BaseModel


class Report(BaseModel):
    reporter: int
    reported: int
