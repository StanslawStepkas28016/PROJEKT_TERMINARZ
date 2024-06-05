from datetime import datetime


class Event:
    def __init__(self, event_date: datetime, description: str, tag: str) -> None:
        self.event_date: datetime = event_date
        self.description: str = description
        self.tag: str = tag

    def __repr__(self) -> str:
        return self.event_date.__str__() + ' ' + self.description.__str__() + ' ' + self.tag.__str__()

    def string_for_file_storing(self) -> str:
        return (self.event_date.year.__str__()
                + '-'
                + self.event_date.month.__str__()
                + '-'
                + self.event_date.day.__str__()
                + '-'
                + self.event_date.hour.__str__()
                + '-'
                + self.event_date.minute.__str__()
                + '|' + self.description.__str__()
                + '|' + (self.tag.__str__() if len(self.tag) > 0 else 'Brak'))
