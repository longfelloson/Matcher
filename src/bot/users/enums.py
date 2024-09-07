from enum import StrEnum


class UserAction(StrEnum):
    report_user = "report_user"
    view_rater_user = "view_rater_user"


class UserStatus(StrEnum):
    reported = "reported"
    blocked = "blocked"
    active = "active"
    not_active = "not_active"
    not_registered = "not_registered"
    left = "left"


class UserGender(StrEnum):
    male = "male"
    female = "female"


class UserProfileSection(StrEnum):
    name = "Имя"
    age = "Возраст"
    city = "Город"
    photo = "Фото"
