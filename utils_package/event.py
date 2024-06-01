from datetime import date


class Event:
    # Tag może być null.
    def __init__(self, event_date: date, description: str, tag: str) -> None:
        self.event_date = event_date
        self.description = description
        self.tag = tag

    # Zwraca string ale bez taga.
    def __repr__(self) -> str:
        return self.event_date.__str__() + ' ' + self.description.__str__() + ' ' + self.tag.__str__()

    def string_for_file_storing(self) -> str:
        return self.event_date.__str__() + '|' + self.description.__str__() + '|' + self.tag.__str__()
