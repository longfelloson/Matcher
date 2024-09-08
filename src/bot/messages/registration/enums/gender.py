from enum import StrEnum


class GenderOption(StrEnum):
    male = "Парень"
    female = "Девушка"


class PreferredGenderOption(StrEnum):
    male = "Парней"
    female = "Девушек"
    both = "Всех"


class PreferredGender(StrEnum):
    male = "male"
    female = "female"
    both = "both"
