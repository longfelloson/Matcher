from pydantic import BaseModel

from bot.users.enums.genders import UserGender, UserViewerGender
from bot.users.registration.enums.gender import PreferredGender


class NewUser(BaseModel):
    id: int | str
    preferred_gender: PreferredGender
    viewer_gender: UserViewerGender
    gender: UserGender
    age: int
    city: str
    