import math
from datetime import datetime, timedelta
from typing import List, Optional

import httpx

from bot.users.models import User
from config import settings

MAX_DISTANCE = 500
DEFAULT_LIMIT = 1
R = 6371  # Radius of the Earth in kilometers


def get_distance_between_locations(first_location: str, second_location: str) -> float:
    lat1, lon1 = map(float, first_location.split(","))
    lat2, lon2 = map(float, second_location.split(","))

    d_lat = math.radians(lat2 - lat1)
    d_lon = math.radians(lon2 - lon1)
    a = (
        math.sin(d_lat / 2) ** 2
        + math.cos(math.radians(lat1))
        * math.cos(math.radians(lat2))
        * math.sin(d_lon / 2) ** 2
    )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c

    return round(distance * 1000)


def get_nearest_user(
    current_user: User,
    users: List[User],
    max_distance: int = MAX_DISTANCE,
) -> User:
    nearest_user = users[0]
    max_search_time = datetime.now() + timedelta(seconds=0.1)

    for other_user in users:
        distance = get_distance_between_locations(
            current_user.location, other_user.location
        )
        if distance < max_distance:
            max_distance = distance
            nearest_user = other_user

        if datetime.now() > max_search_time:
            break
    
    return nearest_user


async def get_city_by_location(latitude: float, longitude: float) -> Optional[str]:
    params = {
        "key": settings.GEOCODER_API_KEY,
        "lat": latitude,
        "lon": longitude,
        "format": "json",
    }
    headers = {
        "accept-language": "ru,en;q=0.9,en-GB;q=0.8,en-US;q=0.7",
    }
    async with httpx.AsyncClient(params=params, headers=headers) as client:
        response = await client.get("https://us1.locationiq.com/v1/reverse")
        return (
            response.json()["address"]["town"] if response.status_code == 200 else None
        )
