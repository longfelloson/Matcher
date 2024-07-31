import random

import pytest
from pydantic import BaseModel

from bot.users.geo.utils import get_nearest_user


def generate_random_location():
    lat = random.uniform(55.5, 55.9)  # Примерный диапазон широты Москвы
    lon = random.uniform(37.3, 37.9)  # Примерный диапазон долготы Москвы
    return f"{lat:.6f}, {lon:.6f}"


class MockUser(BaseModel):
    name: str
    location: str
    distance: int | float = None


names = [
    "Скоба",
    "Бульвар",
    "Горча",
    "Буня",
    "Гордей",
    "Кира",
    "Лев",
    "Мария",
    "Николай",
    "Ольга",
    "Петр",
    "Рита",
]
mock_users = [
    MockUser(name=random.choice(names), location=generate_random_location())
    for _ in range(300000)
]


@pytest.mark.parametrize(
    "user",
    [
        (random.choice(mock_users)),
        (random.choice(mock_users)),
        (random.choice(mock_users)),
        (random.choice(mock_users)),
        (random.choice(mock_users)),
    ],
)
def test_get_nearest_user(user):
    filtered_users = [user_ for user_ in mock_users if user_.name != user.name]
    nearest_user = get_nearest_user(user, filtered_users)

    assert nearest_user.distance <= 500
