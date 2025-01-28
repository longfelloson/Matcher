from typing import (
    Sequence,
    Tuple,
    Generator,
)

from sqlalchemy import or_

from bot.users.enums.statuses import UserStatus
from bot.users.models import User
from bot.users.registration.enums.gender import PreferredGender


def get_age_range(user_age: int) -> Generator:
    return range(user_age - 2, user_age + 3)


def get_search_options(
    rater_users_ids: Sequence[int],
    rated_users_ids: Sequence[int],
    guessed_users_ids: Sequence[int],
    searcher: User,
) -> Tuple:
    minimal_options = [
        User.id.not_in(rater_users_ids),
        User.id != searcher.id,
        User.status == UserStatus.active,
        or_(
            User.viewer_gender == searcher.gender,
            User.viewer_gender == PreferredGender.both,
        ),
    ]
    if searcher.config.guess_age:
        minimal_options.append(
            or_(
                User.id.not_in(guessed_users_ids), 
                User.id.not_in(rated_users_ids)
            )
        )
    else:
        minimal_options.append(User.id.not_in(rated_users_ids))

    search_ages = get_age_range(searcher.age)

    common_options = minimal_options + [User.age.in_(search_ages)]
    specific_options = common_options + [User.city == searcher.city]

    return specific_options, common_options, minimal_options
