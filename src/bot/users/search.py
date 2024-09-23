from operator import and_
from typing import Sequence, Tuple, Generator

from sqlalchemy import or_

from bot.users.enums.genders import UserViewerGender
from bot.users.enums.statuses import UserStatus
from bot.users.models import User
from bot.users.registration.enums.gender import PreferredGender


def get_age_range(user_age: int) -> Generator:
    """Логика для генерации возрастов"""
    return range(user_age - 2, user_age + 3)


def get_search_options(
    rated_users_ids: Sequence[int],
    guessed_users_ids: Sequence[int],
    searcher: User,
) -> Tuple:
    """Получение условий поиска пользователей для просмотра"""
    minimal_options = [
        User.user_id != searcher.user_id,
        User.status == UserStatus.active,
        User.gender == searcher.preferred_gender,
        or_(User.viewer_gender == searcher.gender, User.viewer_gender == PreferredGender.both)
    ]

    if searcher.config.guess_age:
        minimal_options.append(
            or_(
                User.user_id.not_in(guessed_users_ids),
                User.user_id.not_in(rated_users_ids)
            )
        )
    else:
        minimal_options.append(User.user_id.not_in(rated_users_ids))

    search_ages = get_age_range(searcher.age)

    common_options = minimal_options + [
        User.age.in_(search_ages)
    ]
    specific_options = common_options + [
        User.city == searcher.city
    ]

    return specific_options, common_options, minimal_options