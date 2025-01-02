from enum import StrEnum


class GenderOption(StrEnum):
    male = "Мужской"
    female = "Женский"


class PreferredGenderOption(StrEnum):
    male = "Парней"
    female = "Девушек"
    both = "Всех"


class PreferredGender(StrEnum):
    male = "male"
    female = "female"
    both = "both"


class ViewerGenderOption(StrEnum):
    male = "Парни"
    female = "Девушки"
    both = "Все"
