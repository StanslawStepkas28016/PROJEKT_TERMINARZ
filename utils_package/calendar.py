import os

from utils_package.event import Event


class Calendar:
    def __init__(self, calendar_name: str) -> None:
        self.calendar_name = calendar_name
        self.events_list = []

    def add_event(self, event: Event) -> None:
        self.events_list.append(event)

    def remove_event(self, event: Event) -> None:
        self.events_list.remove(event)

    def get_events_sorted_by_date(self) -> list[Event]:
        return sorted(self.events_list, key=lambda event: event.event_date)

    # Metoda nie waliduje podanego taga — dzieje się to w oddzielnym elemencie.
    def get_events_based_on_a_tag(self, input_tag: str) -> list[Event]:
        events_list_based_on_a_tag = []
        for event in self.events_list:
            if event.tag.lower() == input_tag.lower():
                events_list_based_on_a_tag.append(event)
        return events_list_based_on_a_tag

    def store_calendar_in_file(self) -> None:
        with open('files/stored_state.txt', 'w') as file:
            for event in self.events_list:
                print(event.string_to_file(), file=file)

    @staticmethod
    def read_calendar_from_file() -> list[str]:
        with open('files/stored_state.txt', 'r') as file:
            lines = file.read()
            lines = lines.splitlines()

        return lines

    @staticmethod
    def is_anything_stored_in_file() -> bool:
        return os.stat('files/stored_state.txt').st_size == 0

    @staticmethod
    def does_calendar_file_exist() -> bool:
        return os.path.exists('files/stored_state.txt')
