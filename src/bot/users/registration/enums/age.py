from enum import StrEnum, Enum
from typing import Optional, List


class AgeGroup(Enum):
    first = range(10, 14)
    second = range(14, 19)
    third = range(19, 24)
    fourth = range(24, 29)

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
        names = {
            self.first.value: "first",
            self.second.value: "second",
            self.third.value: "third",
            self.fourth.value: "fourth",
        }
        return names[self.value]


class PreferredAgeGroupOption(StrEnum):
    first = "14 - 18"
    second = "19 - 23"
    third = "24 - 28"
