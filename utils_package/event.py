from datetime import datetime


class Event:
    def __init__(self, event_date: datetime, description: str, tag: str) -> None:
        self.event_date: datetime = event_date
        self.description: str = description
        if tag == '':
            self.tag: str = 'Brak'
        else:
            self.tag: str = tag

    def __repr__(self) -> str:
        return self.event_date.__str__() + ' ' + self.description.__str__() + ' ' + self.tag.__str__()

    def modify_event(self, modified_date: datetime, modified_description: str, modified_tag: str) -> None:
        """
        Metoda pozwala modyfikować dane wydarzenia. Jeżeli podane przez użytkownika dane nie są różne
        w stosunku do obecnych danych w wydarzeniu, nie są one modyfikowanie.

        Parameters:
            modified_date (datetime): obiekt zawiera zmodyfikowaną przez użytkownika datę.
            modified_description (str): zawiera zmodyfikowany przez użytkownika opis.
            modified_tag (tag): zawiera zmodyfikowany przez użytkownika tag.
        """

        if self.event_date != modified_date and modified_date != "":
            self.event_date = modified_date
        if self.description != modified_description and modified_description != "":
            self.description = modified_description
        if self.tag != modified_tag and modified_tag != "":
            self.tag = modified_tag

    def string_for_file_storing(self) -> str:
        """
        Metoda pozwala modyfikować dane wydarzenia. Jeżeli podane przez użytkownika dane nie są różne
        w stosunku do obecnych danych w wydarzeniu, nie są one modyfikowanie.

        Returns:
            str: ciąg znakowy, który pozwala na zapisanie obiektu do pliku.
        """

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
                + '|' + self.tag.__str__())
