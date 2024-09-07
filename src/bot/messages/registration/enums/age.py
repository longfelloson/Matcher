from enum import StrEnum, Enum
from typing import Optional, List


class AgeGroup(Enum):
    first = range(14, 19)
    second = range(19, 24)
    third = range(24, 29)

    @classmethod
    def get_group_by_age(cls, age: int) -> Optional["AgeGroup"]:
        for group in cls:
            if age in group.value:
                return group
        return None

    @property
    def ages(self) -> List[int]:
        return list(self.value)  # Convert range to a list

    @property
    def name(self) -> str:
        if self.value == self.first.value:
            return "first"
        elif self.value == self.second.value:
            return "second"
        elif self.value == self.third.value:
            return "third"


class PreferredAgeGroupOption(StrEnum):
    first = "14 - 18"
    second = "19 - 23"
    third = "24 - 28"
