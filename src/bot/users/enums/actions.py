from enum import StrEnum, auto


class UserAction(StrEnum):
    report_user = auto()
    view_rater_user = auto()
    select_captcha_emoji = auto()
