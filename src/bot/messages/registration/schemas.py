from typing import Dict, Optional

from pydantic import Field, BaseModel

from bot.messages.registration.enums.age import PreferredAgeGroupOption, AgeGroup
from bot.messages.registration.enums.gender import (
    GenderOption,
    PreferredGenderOption,
    PreferredGender as PreferredGenderEnum,
)
from bot.users.enums import UserGender as UserGenderEnum


class UserAge(BaseModel):
    age: int = Field(..., ge=14, le=28)


class UserName(BaseModel):
    name: str = Field(..., min_length=2, max_length=15)


class UserGender(BaseModel):
    input: GenderOption

    def convert_input_to_enum(self) -> UserGenderEnum:
        return UserGenderEnum.male if self.input == GenderOption.male else UserGenderEnum.female


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
