from enum import StrEnum


class AdminAction(StrEnum):
    ban_user = "block_user"
    unban_user = "unban_user"
    view_users_amount = "view_users_amount"
    decline_report = "decline_report"
    approve_report = "approve_report"


class AdminPanelSection(StrEnum):
    stats = "stats"
    users = "users"
