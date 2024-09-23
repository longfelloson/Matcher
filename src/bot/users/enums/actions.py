from enum import StrEnum


class UserAction(StrEnum):
    report_user = "report_user"
    view_rater_user = "view_rater_user"
    select_captcha_emoji = "select_captcha_emoji"
