from bot.notifications.keys import USER_SEARCH_OPTIONS_KEY
from bot.notifications.new_users.schemas import NewUser
from bot.storage import storage
from bot.users.enums.genders import UserGender
from bot.users.models import User
from bot.users.registration.enums.gender import PreferredGender
from bot.users.search.utils import get_age_range


def get_new_user_options(new_user: NewUser) -> list[list[str]]:
    base_option = [f"age:{new_user.age}", f"city:{new_user.city}"]
    options = []

    if new_user.preferred_gender == PreferredGender.both:
        for preferred_gender in UserGender:
            options.append(base_option + [
                f"gender:{preferred_gender}", 
                f"preferred_gender:{PreferredGender.both}"
            ])
    else:
        options.append(base_option + [
            f"gender:{new_user.preferred_gender}",
            f"preferred_gender:{new_user.gender}"
        ])
        options.append(base_option + [
            f"gender:{new_user.preferred_gender}",
            f"preferred_gender:{PreferredGender.both}"
        ])

    return options
    

def get_pending_user_options(pending_user: User) -> list[str]:
    options = [
        f"gender:{pending_user.gender}",
        f"city:{pending_user.city}",
        f"preferred_gender:{pending_user.preferred_gender}"
    ]

    for age in get_age_range(pending_user.age):
        options.append(f"age:{age}")

    return options


async def set_pending_user_options(pending_user: User, options: list[str]) -> None:
    await storage.redis.hset(
        USER_SEARCH_OPTIONS_KEY.format(pending_user.id),
        mapping={f"options:{option}": 1 for option in options}
    )

    for option in options:
            await storage.redis.sadd(f"options:{option}", pending_user.id)


async def get_pending_users_ids_by_options(options: list[list[str]]) -> list[int]:
    users_ids = []

    for option in options:
        response = await storage.redis.sinter(*[
            f"options:{name}" for name in option
        ])
        users_ids.extend(response)

    return [int(user_id.decode('utf-8')) for user_id in set(users_ids)]


async def remove_pending_user_options(user_id: int | str) -> None:
    key = USER_SEARCH_OPTIONS_KEY.format(user_id)
    user_sets = await storage.redis.hkeys(key)
    
    for user_set in user_sets:
        await storage.redis.srem(user_set, user_id)

    await storage.redis.delete(key)
