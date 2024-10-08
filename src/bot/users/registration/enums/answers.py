from enum import StrEnum


class SectionAnswer(StrEnum):
    age = "Сколько тебе лет?"
    name = "Как тебя зовут?"
    gender = "Выбери свой пол ⤵️"
    preferred_gender = "Фото какого пола показывать?"
    preferred_age_group = "Какой возраст будешь угадывать?"
    location = "Из какого ты города?"
    photo = "Отправь свое фото ⤵️"
    viewer_gender = "Кто будет просматривать тебя?"
