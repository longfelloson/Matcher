from enum import StrEnum


class ReportStatus(StrEnum):
    DECLINED = "declined"
    APPROVED = "approved"
    PENDING = "pending"


class Answer(StrEnum):
    sent_report = "Жалоба отправлена 📨"
