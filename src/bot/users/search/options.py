from typing import Sequence

from sqlalchemy import or_

from bot.users.enums.genders import UserViewerGender
from bot.users.enums.statuses import UserStatus
from bot.users.models import User
from bot.users.registration.enums.gender import PreferredGender
from bot.users.search.utils import get_age_range


def get_minimal_options(
    rated_users_ids: Sequence[int],
    guessed_users_ids: Sequence[int],
    searcher: User,
) -> list:
    options = [
        User.id != searcher.id,
        User.status == UserStatus.active,
        or_(
            searcher.preferred_gender == User.gender,
            searcher.preferred_gender == PreferredGender.both,
        ),
        or_(
            User.viewer_gender == searcher.gender,
            User.viewer_gender == UserViewerGender.both,
        ),
    ]

    if searcher.config.guess_age:
        options.append(
            or_(
                User.id.not_in(guessed_users_ids),
                User.id.not_in(rated_users_ids)
            )
        )
    else:
        options.append(User.id.not_in(rated_users_ids))

    return options


def get_search_options(
    rated_users_ids: Sequence[int],
    guessed_users_ids: Sequence[int],
    searcher: User,
) -> list:
    minimal_options = get_minimal_options(
        rated_users_ids, guessed_users_ids, searcher
    )

    search_ages = get_age_range(searcher.age)
    extended_search_ages = get_age_range(searcher.age, extend=True)
    
    common_options = minimal_options + [
        User.age.in_(search_ages)
    ]
    extended_options = common_options + [
        User.age.in_(extended_search_ages)
    ]
    specific_options = common_options + [
        User.city == searcher.city
    ]

    return [
        specific_options, 
        extended_options, 
        common_options, 
        minimal_options,
    ]
