from pydantic import BaseModel


class Location(BaseModel):
    latitude: float
    longitude: float

    def get_values(self):
        return tuple(value for value in self)
