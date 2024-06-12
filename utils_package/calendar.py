import os

from utils_package.event import Event
from utils_package.data_validator import Validator
import utils_package.data_parser as Parser
from colorama import Fore, Style
from datetime import datetime


class Calendar:
    """
    Klasa służy do przechowywania obiektów klasy Event,
    zapewniając jednocześnie funkcjonalności potrzebne dla programu.
    """

    def __init__(self) -> None:
        self.events_list: list[Event] = []

    def add_event(self, event: Event) -> None:
        """
        Metoda dodaje wydarzenie (obiekt klasy Event),
        do listy wydarzeń (pola klasowego).

        Parameters:
            event (Event): obiekt klasy Event.
        """

        self.events_list.append(event)

    def get_event_by_index(self, event_index: int) -> Event:
        """
        Metoda pozwala na pozyskanie elementu pod danym indeksem,
        w liście wydarzeń.

        Parameters:
            event_index (int): indeks, pod którym znajduje się element w liście.

        Returns:
            event (Event): obiekt klasy Event.
        """

        return self.events_list[event_index]

    def remove_event(self, event_index: int) -> bool:
        """
        Metoda pozwala na usuwanie elementu pod danym indeksem,
        w liście wydarzeń.

        Parameters:
            event_index (int): indeks, pod którym znajduje się element w liście.

        Returns:
            bool: typ bool, który służy do zwalidowania, czy podany w parametrze
            metody indeks, jest poprawny.

        Raises:
            IndexError: podany przez użytkownika indeks jest spoza listy.
        """

        try:
            self.events_list.pop(event_index)
        except IndexError:
            return False

        return True

    def modify_event_validation(self, event_index: int) -> bool:
        """
        Metoda pozwala na walidację, czy dane wydarzenie znajduje się
        w liście wydarzeń

        Parameters:
            event_index (int): indeks, pod którym potencjalnie znajduje się element w liście.

        Returns:
            bool: typ bool, który służy do zwalidowania, czy podany w parametrze
            metody indeks, jest poprawny.

        Raises:
            IndexError: podany przez użytkownika indeks jest spoza listy.
        """

        try:
            self.events_list[event_index]
        except IndexError:
            return False

        return True

    def get_events_sorted_by_date(self) -> list[Event]:
        """
        Metoda zwraca listę wydarzeń posortowanych
        po dacie (rosnąco).

        Returns:
            list[Event]: lista wydarzeń posortowanych po dacie rosnąco.
        """

        return sorted(self.events_list, key=lambda event: event.event_date)

    def get_events_sorted_by_tag(self, input_tag: str) -> list[Event]:
        """
        Metoda zwraca listę wydarzeń posortowanych po podanym przez użytkownika tagu.

        Parameters:
            input_tag (str): podany przez użytkownika tag.

        Returns:
            list[Event]: lista wydarzeń posortowana po tagu.
        """

        events_list_based_on_a_tag = []
        for event in self.events_list:
            if event.tag.lower() == input_tag.lower():
                events_list_based_on_a_tag.append(event)
        return events_list_based_on_a_tag

    def get_events_in_specific_date(self, input_date: datetime) -> list[Event]:
        """
        Metoda zwraca listę wydarzeń w danym dniu (dacie)

        Parameters:
            input_date (datetime): podana przez użytkownika data.

        Returns:
            list[Event]: lista wydarzeń, które wystąpiły danego dnia.
        """

        event_list_based_on_specific_date = []
        for event in self.events_list:
            if (event.event_date.day == input_date.day
                    and event.event_date.month == input_date.month
                    and event.event_date.year == input_date.year):
                event_list_based_on_specific_date.append(event)

        return event_list_based_on_specific_date

    def get_events_in_date_range(self, input_date_from: datetime, input_date_to: datetime) -> list[Event]:
        """
        Metoda zwraca listę wydarzeń w zakresie dni podanych przez użytkownika.

        Parameters:
            input_date_from (datetime): podana przez użytkownika data od.
            input_date_to (datetime): podana przez użytkownika data do.

        Returns:
            list[Event]: lista wydarzeń, które wystąpiły w podanym przedziale dni.
        """

        event_list_based_on_date_range = []
        for event in self.events_list:
            if (input_date_from.year <= event.event_date.year <= input_date_to.year
                    and input_date_from.month <= event.event_date.month <= input_date_to.month
                    and input_date_from.day <= event.event_date.day <= input_date_to.day):
                event_list_based_on_date_range.append(event)

        return event_list_based_on_date_range

    def store_calendar_in_file(self) -> None:
        """
        Metoda zapisuje obecną listę wydarzeń do pliku.
        """

        if not Validator.does_calendar_file_exist():
            os.makedirs('files', exist_ok=True)
            with open('files/stored_state.txt', 'w') as file:
                for event in self.events_list:
                    print(event.string_for_file_storing(), file=file)
        else:
            with open('files/stored_state.txt', 'w') as file:
                for event in self.events_list:
                    print(event.string_for_file_storing(), file=file)

    @staticmethod
    def print_events_in_provided_list(events_list: list[Event]) -> None:
        """
        Metoda wypisuje na konsole wydarzenia w podanej liście.

        Parameters:
            events_list (list[Event]): lista wydarzeń.
        """

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
        """
        Metoda czyta z pliku, tworzy nowy obiekt klasy Calendar i inicjuje
        listę wydarzeń tego obiektu.

        Returns:
            Calendar: obiekt klasy Calendar, z wypełnioną wydarzeniami listą wydarzeń (z pliku).
        """

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
