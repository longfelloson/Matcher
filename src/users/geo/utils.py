import heapq
import random
from datetime import datetime, timedelta
from typing import List, Optional

import httpx
import numpy as np

from src import config
from src.users.geo.schemas import Location
from src.users.models import User

from geopy.distance import geodesic

DEFAULT_RADIUS = 500
DEFAULT_LIMIT = 1


def get_user_location(user: User) -> Location:
    """
    Получение объекта пользовательской локации
    """
    return Location(longitude=float(user.location.split("*")[0]), latitude=float(user.location.split("*")[1]))


def get_nearest_user(current_user: User, users: List[User], radius: int = DEFAULT_RADIUS, limit: int = 1) -> User:
    """
    Получение ближайшего пользователя к заданному из списка других пользователей.
    """
    max_distance, nearest_user = radius, users[0]
    max_search_time = datetime.now() + timedelta(seconds=0.1)

    for other_user in users:
        if (distance := get_distance_between_users(current_user, other_user)) < max_distance:
            max_distance = distance
            nearest_user = other_user

        if datetime.now() > max_search_time:
            nearest_user.distance = max_distance
            return nearest_user

    nearest_user.distance = max_distance
    return nearest_user


def get_distance_between_users(first_user: User, second_user: User) -> float:
    """
    Получение расстояние между двумя точками
    """
    first_user_loc_values = tuple(get_user_location(first_user).model_dump().values())
    second_user_loc_values = tuple(get_user_location(second_user).model_dump().values())
    return geodesic(first_user_loc_values, second_user_loc_values).meters


async def reverse_geocode_user_location(location: Location) -> Optional[str]:
    """
    Получение информации о пользовательской локации
    """
    params = {
        "key": config.GEOCODER_API_KEY,
        "lat": location.latitude,
        "lon": location.longitude,
        "format": "json"
    }
    headers = {
        'accept-language': 'ru,en;q=0.9,en-GB;q=0.8,en-US;q=0.7',
    }
    async with httpx.AsyncClient(params=params, headers=headers) as client:
        response = await client.get('https://us1.locationiq.com/v1/reverse')
        return response.json()['address']['town'] if response.status_code == 200 else None
