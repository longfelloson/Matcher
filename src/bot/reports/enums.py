from enum import StrEnum


class ReportStatus(StrEnum):
    DECLINED = "declined"
    APPROVED = "approved"
    PENDING = "pending"


class Answer:
    sent_report = "Жалоба отправлена 📨"
