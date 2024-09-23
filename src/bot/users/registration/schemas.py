from typing import Dict, Optional

from pydantic import Field, BaseModel

from bot.users.registration.constants import MIN_AGE
from bot.users.registration.enums.age import PreferredAgeGroupOption, AgeGroup
from bot.users.registration.enums.gender import (
    GenderOption,
    PreferredGenderOption,
    PreferredGender as PreferredGenderEnum,
    ViewerGenderOption,
)
from bot.users.enums.genders import UserGender as UserGenderEnum, UserViewerGender as UserViewerGenderEnum


class UserAge(BaseModel):
    age: int = Field(..., ge=MIN_AGE)


class UserName(BaseModel):
    name: str = Field(..., min_length=2, max_length=15)


class UserGender(BaseModel):
    input: GenderOption

    def convert_input_to_enum(self) -> UserGenderEnum:
        return UserGenderEnum.male if self.input == GenderOption.male else UserGenderEnum.female


class UserViewerGender(BaseModel):
    input: ViewerGenderOption

    def convert_input_to_enum(self) -> UserGenderEnum:
        mapping: Dict[ViewerGenderOption, UserViewerGenderEnum] = {
            ViewerGenderOption.female: UserViewerGenderEnum.female,
            ViewerGenderOption.male: UserViewerGenderEnum.male,
            ViewerGenderOption.both: UserViewerGenderEnum.both
        }
        return mapping.get(self.input)


class UserPreferredGender(BaseModel):
    input: PreferredGenderOption

    def convert_input_to_enum(self) -> Optional[PreferredGenderEnum]:
        mapping: Dict[PreferredAgeGroupOption, AgeGroup] = {
            PreferredGenderOption.male: PreferredGenderEnum.male,
            PreferredGenderOption.female: PreferredGenderEnum.female,
            PreferredGenderOption.both: PreferredGenderEnum.both,
        }
        return mapping.get(self.input)


class UserPreferredAgeGroup(BaseModel):
    input: PreferredAgeGroupOption

    def convert_input_to_enum(self) -> AgeGroup:
        mapping: Dict[PreferredAgeGroupOption, AgeGroup] = {
            PreferredAgeGroupOption.first: AgeGroup.first.name,
            PreferredAgeGroupOption.second: AgeGroup.second.name,
            PreferredAgeGroupOption.third: AgeGroup.third.name,
        }
        return mapping.get(self.input)


class UserCity(BaseModel):
    city: str = Field(min_length=2, max_length=23)


class UserRegistrationInfo(BaseModel):
    user_id: int
    age: int
    name: str
    gender: UserGenderEnum
    preferred_gender: PreferredGenderEnum
    viewer_gender: UserViewerGenderEnum
    photo_url: str
    city: str
    location: str = None
