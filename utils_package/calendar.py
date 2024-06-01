import os

from utils_package.event import Event
from utils_package.data_parser import Parser


class Calendar:
    def __init__(self, calendar_name: str) -> None:
        self.calendar_name: str = calendar_name
        self.events_list: list[Event] = []

    def add_event(self, event: Event) -> None:
        self.events_list.append(event)

    def remove_event(self, event_index: int) -> bool:
        try:
            self.events_list.pop(event_index)
        except IndexError:
            return False

        return True

    def get_events_sorted_by_date(self) -> list[Event]:
        return sorted(self.events_list, key=lambda event: event.event_date)

    # Metoda nie waliduje podanego taga — dzieje się to w oddzielnym elemencie.
    def get_events_based_on_a_tag(self, input_tag: str) -> list[Event]:
        events_list_based_on_a_tag = []
        for event in self.events_list:
            if event.tag.lower() == input_tag.lower():
                events_list_based_on_a_tag.append(event)
        return events_list_based_on_a_tag

    # Metoda bierze już w jakiś sposób posortowaną listę, więc dlatego przyjmuje ją
    @staticmethod
    def print_events_in_provided_list(events_list: list[Event]) -> None:
        count: int = 0
        for e in events_list:
            elem_to_print: str = count.__str__() + '. ' + e.event_date.__str__() + ' ' + e.description.__str__()

            if e.tag is None:
                print(elem_to_print)
            else:
                print(elem_to_print + ' ' + e.tag.__str__())

            count += 1

    def store_calendar_in_file(self) -> None:
        with open('files/stored_state.txt', 'w') as file:
            for event in self.events_list:
                print(event.string_to_file(), file=file)

    # Statyczny "konstruktor", czyta, to co jest w pliku, następnie parsuje dane do pliku,
    # zwracając obiekt typu Calendar, który posiada już dodane (do listy) obiekty klasy Event
    @staticmethod
    def read_calendar_from_file_and_return_calendar_filled_with_events() -> 'Calendar':
        with open('files/stored_state.txt', 'r') as file:
            file_contents: list[str] = file.read().split('\n')
            event_list: list[Event] = []
            calendar: Calendar

            for line in file_contents:
                split: list[str] = line.split("|")
                if split.__len__() == 3:
                    event_list.append(Event(Parser.parse_event_date_from_input(split[0]), split[1], split[2]))
                else:
                    calendar = Calendar(line)

            for event in event_list:
                calendar.add_event(event)

        return calendar

    @staticmethod
    def is_anything_stored_in_file() -> bool:
        return os.stat('files/stored_state.txt').st_size == 0

    @staticmethod
    def does_calendar_file_exist() -> bool:
        return os.path.exists('files/stored_state.txt')
