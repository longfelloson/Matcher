from enum import StrEnum, auto


class MailingAction(StrEnum):
    do = auto()
    input_text = auto()
    confirm = auto()
    decline = auto()

    @property
    def name(self) -> str:
        names = {
            self.do: "Провести рассылку",
            self.input_text: "Ввести текст для рассылки",
            self.confirm: "Подтвердить рассылку",
            self.decline: "Отменить рассылку",
        }
        return names[self]
