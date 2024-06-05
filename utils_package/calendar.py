from utils_package.event import Event
from utils_package.data_parser import Parser
from colorama import Fore, Style
from datetime import datetime


class Calendar:
    def __init__(self) -> None:
        self.events_list: list[Event] = []

    def add_event(self, event: Event) -> None:
        self.events_list.append(event)

    def get_event_by_index(self, event_index: int) -> Event:
        return self.events_list[event_index]

    def remove_event(self, event_index: int) -> bool:
        try:
            self.events_list.pop(event_index)
        except IndexError:
            return False

        return True

    def modify_event_validation(self, event_index: int) -> bool:
        try:
            self.events_list[event_index]
        except IndexError:
            return False

        return True

    def get_events_sorted_by_date(self) -> list[Event]:
        return sorted(self.events_list, key=lambda event: event.event_date)

    # Metoda nie waliduje podanego taga — dzieje się to w oddzielnym elemencie.
    def get_events_sorted_by_tag(self, input_tag: str) -> list[Event]:
        events_list_based_on_a_tag = []
        for event in self.events_list:
            if event.tag.lower() == input_tag.lower():
                events_list_based_on_a_tag.append(event)
        return events_list_based_on_a_tag

    def get_events_in_specific_date(self, input_date: datetime) -> list[Event]:
        event_list_based_on_specific_date = []
        for event in self.events_list:
            if (event.event_date.day == input_date.day
                    and event.event_date.month == input_date.month
                    and event.event_date.year == input_date.year):
                event_list_based_on_specific_date.append(event)

        return event_list_based_on_specific_date

    def get_events_in_date_range(self, input_date_from: datetime, input_date_to: datetime) -> list[Event]:
        event_list_based_on_date_range = []
        for event in self.events_list:
            if (input_date_from.year <= event.event_date.year <= input_date_to.year
                    and input_date_from.month <= event.event_date.month <= input_date_to.month
                    and input_date_from.day <= event.event_date.day <= input_date_to.day):
                event_list_based_on_date_range.append(event)

        return event_list_based_on_date_range

    def store_calendar_in_file(self) -> None:
        with open('files/stored_state.txt', 'w') as file:
            for event in self.events_list:
                print(event.string_for_file_storing(), file=file)

    @staticmethod
    def print_events_in_provided_list(events_list: list[Event]) -> None:
        count: int = 1
        for e in events_list:
            elem_to_print: str = (count.__str__()
                                  + '. ' + Fore.LIGHTYELLOW_EX + 'Data wydarzenia: ' + Style.RESET_ALL
                                  + e.event_date.__str__()
                                  + ', ' + Fore.LIGHTYELLOW_EX + 'Opis wydarzenia: ' + Style.RESET_ALL
                                  + e.description.__str__())

            print(elem_to_print + ', ' + Fore.LIGHTYELLOW_EX + 'Tag: ' + Style.RESET_ALL + e.tag.__str__())
            count += 1

    @staticmethod
    def read_calendar_from_file_and_return_calendar_filled_with_events() -> 'Calendar':
        with open('files/stored_state.txt', 'r') as file:
            file_contents: list[str] = file.read().strip().split('\n')
            event_list: list[Event] = []
            calendar: Calendar = Calendar()

            for line in file_contents:
                split: list[str] = line.split('|')
                event_list.append(
                    Event(Parser.parse_event_date_from_string_input_with_hour_and_minutes(split[0]), split[1],
                          split[2]))
            for event in event_list:
                calendar.add_event(event)

        return calendar
