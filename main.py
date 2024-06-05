from datetime import datetime
from os import system, name
from time import sleep

from colorama import Fore, Style

from utils_package.event import Event
from utils_package.calendar import Calendar
from utils_package.data_parser import Parser
from utils_package.data_validator import Validator


def main() -> None:
    existing_user: bool = Validator.does_calendar_file_exist() and not Validator.is_calendar_file_empty()
    handle_user(existing_user)


def handle_user(existing_user: bool) -> None:
    # Sprawdzenie, czy kalendarz istnieje z oddzielną obsługą dla obu przypadków.
    calendar: Calendar
    if existing_user:
        calendar = Calendar.read_calendar_from_file_and_return_calendar_filled_with_events()
    else:
        calendar = Calendar()
        clear_terminal()

    # Pętla wyświetlająca dostępne opcje, z logiką działania programu i walidacją.
    while True:
        print_main_menu()
        option_etiquette = int(input('Wprowadź etykietę opcji : '))

        if option_etiquette > 5 or option_etiquette < 1:
            handle_wrong_option()
        elif option_etiquette == 1:
            handle_add_to_calendar(calendar)
        elif option_etiquette == 2:
            handle_modify_events_within_calendar(calendar)
        elif option_etiquette == 3:
            handle_delete_from_calendar(calendar)
        elif option_etiquette == 4:
            handle_display_from_calendar(calendar)
        elif option_etiquette == 5:
            handle_quit_app(calendar)
            break

        clear_terminal()


def handle_quit_app(calendar: Calendar) -> None:
    calendar.store_calendar_in_file()
    print_log('Kalendarz zapisany!')


def handle_display_from_calendar(calendar: Calendar) -> None:
    clear_terminal()
    print_info('Wybór wydarzeń :')
    print('1. Sortowanie po dacie wydarzeń.')
    print('2. Na podstawie taga.')
    sort_type: int = int(input('Wprowadź swój wybór : '))

    while not (sort_type == 1 or sort_type == 2):
        clear_terminal()
        print_error('Podano niepoprawny typ sortowania!')
        sleep(2)
        clear_terminal()
        print_info('Wybór wydarzeń :')
        print('1. Sortowanie po dacie wydarzeń.')
        print('2. Na podstawie taga.')
        sort_type = int(input('Wprowadź swój wybór : '))

    clear_terminal()
    print_info('Wydarzenia w terminarzu : ')
    if sort_type == 1:
        Calendar.print_events_in_provided_list(calendar.get_events_sorted_by_date())
    elif sort_type == 2:
        input_tag: str = input('Podaj tag : ')
        events_list: list[Event] = calendar.get_events_sorted_by_tag(input_tag)
        if len(events_list) == 0:
            print_error('Brak wydarzeń zgodnych z podanym tagiem!')
        else:
            Calendar.print_events_in_provided_list(events_list)

    input('Żeby wrócić do menu, naciśnij enter : ')


def handle_delete_from_calendar(calendar: Calendar) -> None:
    # Pobranie wydarzeń z kalendarza, razem z wprowadzeniem numeru zdarzenia do usunięcia.
    print_info('Dostępne wydarzenia :')
    events_list: list[Event] = calendar.get_events_sorted_by_date()
    calendar.print_events_in_provided_list(events_list)
    event_index: int = int(input('Wprowadź numer wydarzenia do usunięcia : '))
    # Walidacja wprowadzonego numeru.
    removed: bool = calendar.remove_event(event_index - 1)
    while not removed:
        print_error('Podano niepoprawny numer zdarzenia do usunięcia!')
        input('Żeby podać ponownie, naciśnij enter : ')
        clear_terminal()
        event_index = int(input('Wprowadź numer wydarzenia do usunięcia : '))
        removed = calendar.remove_event(event_index - 1)
    # Log dotyczący usunięcia.
    print_log('Zmiany zapisane!')
    input('Żeby wrócić do menu, naciśnij enter : ')


def handle_modify_events_within_calendar(calendar: Calendar) -> None:
    # Wylistowanie dostępnych wydarzeń kalendarzu
    clear_terminal()
    print_info('Dostępne wydarzenia, które można modyfikować :')
    events_list: list[Event] = calendar.get_events_sorted_by_date()
    calendar.print_events_in_provided_list(events_list)
    event_index: int = int(input('Wprowadź numer wydarzenia do modyfikacji : '))
    # Walidacja wprowadzonego numeru.
    found_in_list: bool = calendar.modify_event_validation(event_index - 1)
    while not found_in_list:
        print_error('Podano niepoprawny numer zdarzenia do modyfikacji!')
        input('Żeby podać ponownie, naciśnij enter : ')
        clear_terminal()
        print_info('Dostępne wydarzenia, które można modyfikować :')
        calendar.print_events_in_provided_list(events_list)
        event_index = int(input('Wprowadź numer wydarzenia do modyfikacji : '))
        found_in_list = calendar.modify_event_validation(event_index - 1)
    # Wprowadzenie danych do zmiany przez użytkownika.
    clear_terminal()
    returned_event: Event = calendar.get_event_by_index(event_index - 1)
    # Pobranie nowej daty, wraz z walidacją, od użytkownika.
    print(Fore.LIGHTYELLOW_EX + 'Obecna data : ' + Style.RESET_ALL + str(returned_event.event_date))
    modified_date_string: str = str(
        input('Jeżeli chcesz zmodyfikować datę, wpisz nową datę (YYYY-MM-DD-HH-MN), jeśli nie, naciśnij enter : '))
    modified_date: datetime
    if modified_date_string == '':
        modified_date = returned_event.event_date
    else:
        # Emulacja pętli do-while, służąca do walidacji wprowadzonej daty.
        date_validated: bool = Validator.date_validation(modified_date_string)
        while not date_validated:
            print_error('Podano niepoprawną datę!')
            input('Żeby podać ponownie, naciśnij enter : ')
            clear_terminal()
            print(Fore.LIGHTYELLOW_EX + 'Obecna data : ' + Style.RESET_ALL + str(returned_event.event_date))
            modified_date_string = str(input(
                'Jeżeli chcesz zmodyfikować datę, wpisz nową datę (YYYY-MM-DD-HH-MN), jeśli nie, naciśnij enter : '))
            date_validated = Validator.date_validation(modified_date_string)
        modified_date = Parser.parse_event_date_from_string_input(modified_date_string)
    # Pobranie nowego opisu od użytkownika.
    print(Fore.LIGHTYELLOW_EX + 'Obecny opis : ' + Style.RESET_ALL + returned_event.description)
    modified_description = str(input('Jeżeli chcesz zmodyfikować opis, wpisz nowy opis, jeśli nie, naciśnij enter : '))
    # Pobranie nowego taga od użytkownika.
    print(Fore.LIGHTYELLOW_EX + 'Obecny tag : ' + Style.RESET_ALL + returned_event.tag)
    modified_tag = str(input('Jeżeli chcesz zmodyfikować opis, wpisz nowy opis, jeśli nie, naciśnij enter : '))
    # Modyfikacja obiektu.
    returned_event.modify_event(modified_date, modified_description, modified_tag)
    # Log dotyczący zmian.
    clear_terminal()
    print_log('Zmiany zapisane!')
    input('Żeby wrócić do menu, naciśnij enter : ')


def handle_add_to_calendar(calendar: Calendar) -> None:
    # Pobranie daty wydarzenia i oczyszczenie terminalu.
    clear_terminal()
    event_date_str: str = (str(input('Podaj datę wydarzenia (YYYY-MM-DD-HH-MN) : ')))
    # Emulacja pętli do-while, służąca do walidacji wprowadzonej daty.
    date_validated: bool = Validator.date_validation(event_date_str)
    while not date_validated:
        print_error('Podano niepoprawną datę!')
        input('Żeby podać ponownie, naciśnij enter : ')
        clear_terminal()
        event_date_str: str = (str(input('Podaj datę wydarzenia (YYYY-MM-DD) : ')))
        date_validated = Validator.date_validation(event_date_str)
    # Ustalenie zwalidowanej daty.
    event_date: datetime = Parser.parse_event_date_from_string_input(event_date_str)
    # Pobranie danych, bez potrzeby walidacji.
    description = str(input('Wprowadź opis zdarzenia : '))
    tag = str(input('Wprowadź tag zdarzenia (opcjonalne), wciśnij enter, jeżeli nie chcesz : '))
    # Dodanie danych do kalendarza, wraz z odpowiednim logiem.
    calendar.add_event(Event(event_date, description, tag))
    clear_terminal()
    print_log('Dodano wydarzenie do terminarza :)')
    input('Żeby wrócić do menu, naciśnij enter : ')


def handle_wrong_option() -> None:
    # Podana została niepoprawna etykieta opcji.
    print_error('Podano niepoprawną etykietę opcji!')
    input('Żeby wrócić, naciśnij enter : ')


def print_main_menu() -> None:
    print(Fore.LIGHTMAGENTA_EX + 'Dostępne opcje :' + Style.RESET_ALL)
    print('1. Dodaj wydarzenie do terminarza.')
    print('2. Modyfikuj wydarzenie z terminarza.')
    print('3. Usuń wydarzenie z terminarza.')
    print('4. Wylistuj wydarzenie z terminarza.')
    print('5. Zakończ pracę programu.')


def print_error(error_information: str) -> None:
    print(Fore.LIGHTRED_EX + error_information + Style.RESET_ALL)


def print_log(log_information: str) -> None:
    print(Fore.LIGHTGREEN_EX + log_information + Style.RESET_ALL)


def print_info(info_information: str) -> None:
    print(Fore.LIGHTMAGENTA_EX + info_information + Style.RESET_ALL)


def clear_terminal():
    system('cls' if name == 'nt' else 'clear')


if __name__ == '__main__':
    main()
