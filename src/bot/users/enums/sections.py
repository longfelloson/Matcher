from enum import StrEnum


class UserProfileSection(StrEnum):
    name = "Имя"
    age = "Возраст"
    city = "Город"
    photo = "Фото"
    gender = "Пол"
    preferred_gender = "Кого просматривать?"
    viewer_gender = "Кто будет просматривать?"
