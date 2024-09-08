from enum import Enum


class ReportStatus(str, Enum):
    viewed = "viewed"
    not_viewed = "not_viewed"
