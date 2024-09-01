from enum import Enum
from typing import List, Optional


class UserAction(str, Enum):
    report_user = "report_user"
    change_config = "change_config"
    view_rater_user = "view_rater_user"


class UserStatus(str, Enum):
    blocked = "blocked"
    active = "active"
    not_registered = "not_registered"


class UserGender(str, Enum):
    male = "male"
    female = "female"


class PreferredGender(str, Enum):
    male = "male"
    female = "female"
    both = "both"


class PreferredAgeGroup(str, Enum):
    first = "first"
    second = "second"
    third = "third"

    class Age(str, Enum):
        first = "14 - 18"
        second = "19 - 23"
        third = "24 - 28"


class AgeGroup(Enum):
    FIRST = [14, 15, 16, 17, 18]
    SECOND = [19, 20, 21, 22, 23]
    THIRD = [24, 25, 26, 27, 28]

    def __str__(self):
        return self.name.lower()

    @property
    def ages(self) -> List[int]:
        return self.value

    @classmethod
    def get_group_by_age(cls, age: int) -> Optional["AgeGroup"]:
        for group in cls:
            if age in group.ages:
                return group
        return None
