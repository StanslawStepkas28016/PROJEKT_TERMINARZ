from datetime import datetime
from os import system, name
from colorama import Fore, Style

from utils_package.event import Event
from utils_package.calendar import Calendar
import utils_package.data_parser as Parser
from utils_package.data_validator import Validator


def main() -> None:
    """
    Metoda sprawdza, czy użytkownik posiada już swój kalendarz i przekazuje parametr do kolejnej metody.
    """

    # Sprawdzenie, czy użytkownik istnieje (czy posiada plik z danymi z kalendarza)
    existing_user: bool = Validator.does_calendar_file_exist() and not Validator.is_calendar_file_empty()
    handle_user(existing_user)


def handle_user(existing_user: bool) -> None:
    """
    Metoda w zależności od tego, czy istnieje plik przechowujący dane kalendarza, czyta dane z pliku, bądź fabrykuje
    nowy obiekt klasy Calendar. Dodatkowo metoda przeprowadza operacje wejścia-wyjścia, walidując wprowadzone
    przez użytkownika dane etykiety opcji.
    """

    # Obsługa przypadków dla istniejącego i nowego użytkownika.
    calendar: Calendar
    if existing_user:
        calendar = Calendar.read_calendar_from_file_and_return_calendar_filled_with_events()
    else:
        calendar = Calendar()
        clear_terminal()

    # Pętla wyświetlająca dostępne opcje, z logiką działania programu i walidacją.
    while True:
        print_main_menu()

        try:
            option_etiquette = int(input('Wprowadź etykietę opcji : '))
        except ValueError:
            print_error('Można wprowadzać tylko wartości numeryczne!')
            input('Żeby podać ponownie, naciśnij enter : ')
            clear_terminal()
            continue

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
    """
    Metoda zapisuje stan kalendarza do pliku, korzystając
    z metody w klasie Calendar oraz wypisuje odpowiednią informację użytkownikowi.
    """

    calendar.store_calendar_in_file()
    print_log('Kalendarz zapisany!')


def handle_display_from_calendar(calendar: Calendar) -> None:
    """
    Metoda realizuje funkcjonalność wyświetlania danych zapisanych w kalendarzu,
    na podstawie podanej przez użytkownika etykiety opcji. Na każdym etapie wprowadzania
    danych, przeprowadzana jest walidacja, która zapobiega wprowadzeniu niepoprawnych danych.
    """

    clear_terminal()
    print_info('Wybór wydarzeń :')
    print('1. Sortowanie po dacie wydarzeń.')
    print('2. Na podstawie przedziału dni.')
    print('3. Na podstawie jednego dnia.')
    print('4. Na podstawie taga.')

    try:
        display_type: int = int(input('Wprowadź swój wybór : '))
    except ValueError:
        print_error('Można wprowadzać tylko wartości numeryczne!')

    # Walidacja wprowadzonej etykiety opcji.
    while display_type > 4 or display_type < 1:
        clear_terminal()
        print_error('Podano niepoprawny typ sortowania!')
        input('Żeby podać ponownie, naciśnij enter : ')
        clear_terminal()
        print_info('Wybór wydarzeń :')
        print('1. Sortowanie po dacie wydarzeń.')
        print('2. Na podstawie przedziału dni.')
        print('3. Na podstawie jednego dnia.')
        print('4. Na podstawie taga.')
        display_type = int(input('Wprowadź swój wybór : '))

    # Wypisanie odpowiednich informacji na konsole, w zależności od wybranej opcji.
    clear_terminal()
    print_info('Wydarzenia w terminarzu : ')
    if display_type == 1:
        Calendar.print_events_in_provided_list(calendar.get_events_sorted_by_date())
    elif display_type == 2:
        from_to_str: str = str(input('Wprowadź przedział datowy (YYYY-MM-DD YYYY-MM-DD) : '))
        from_to_list: list[str] = from_to_str.split(' ')
        from_valid: bool = Validator.date_validation_without_hours_and_minutes(from_to_list[0])
        to_valid: bool = Validator.date_validation_without_hours_and_minutes(from_to_list[1])

        while not from_valid and not to_valid:
            print_error('Podano niepoprawne daty, upewnij się, że oddzielasz je spacją!')
            input('Żeby podać ponownie, naciśnij enter : ')
            clear_terminal()
            from_to_str: str = str(input('Wprowadź przedział datowy (YYYY-MM-DD YYYY-MM-DD) : '))
            from_to_list = from_to_str.split(' ')
            from_valid = Validator.date_validation_without_hours_and_minutes(from_to_list[0])
            to_valid = Validator.date_validation_without_hours_and_minutes(from_to_list[1])

        from_date: datetime = Parser.parse_event_date_from_string_input_without_hours_and_minutes(from_to_list[0])
        to_date: datetime = Parser.parse_event_date_from_string_input_without_hours_and_minutes(from_to_list[1])
        events_in_dates_range: list[Event] = calendar.get_events_in_date_range(from_date, to_date)
        Calendar.print_events_in_provided_list(events_in_dates_range)
    elif display_type == 3:
        date_at_str: str = str(input('Wprowadź datę YYYY-MM-DD : '))
        date_at_valid: bool = Validator.date_validation_without_hours_and_minutes(date_at_str)

        while not date_at_valid:
            print_error('Podano niepoprawną datę!')
            input('Żeby podać ponownie, naciśnij enter : ')
            clear_terminal()
            date_at_str = str(input('Wprowadź datę YYYY-MM-DD : '))
            date_at_valid = Validator.date_validation_without_hours_and_minutes(date_at_str)

        events_based_on_day: list[Event] = calendar.get_events_in_specific_date(
            Parser.parse_event_date_from_string_input_without_hours_and_minutes(date_at_str))
        Calendar.print_events_in_provided_list(events_based_on_day)
    elif display_type == 4:
        input_tag: str = input('Podaj tag : ')
        events_list: list[Event] = calendar.get_events_sorted_by_tag(input_tag)
        if len(events_list) == 0:
            print_error('Brak wydarzeń zgodnych z podanym tagiem!')
        else:
            Calendar.print_events_in_provided_list(events_list)

    input('Żeby wrócić do menu, naciśnij enter : ')


def handle_delete_from_calendar(calendar: Calendar) -> None:
    """
    Metoda obsługuje funkcjonalność usuwania danych z kalendarza,
    przeprowadza walidację wprowadzonych danych oraz wyświetla odpowiednie informacje.

    Parameters:
        calendar (Calendar): obiekt klasy kalendarz.
    """
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
    """
    Metoda obsługuje funkcjonalność modyfikowania danych w kalendarzu,
    przeprowadza walidację wprowadzonych danych oraz wyświetla odpowiednie informacje.

    Parameters:
        calendar (Calendar): obiekt klasy kalendarz.
    """
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
        date_validated: bool = Validator.date_validation_with_hour_and_minutes(modified_date_string)
        while not date_validated:
            print_error('Podano niepoprawną datę!')
            input('Żeby podać ponownie, naciśnij enter : ')
            clear_terminal()
            print(Fore.LIGHTYELLOW_EX + 'Obecna data : ' + Style.RESET_ALL + str(returned_event.event_date))
            modified_date_string = str(input(
                'Jeżeli chcesz zmodyfikować datę, wpisz nową datę (YYYY-MM-DD-HH-MN), jeśli nie, naciśnij enter : '))
            date_validated = Validator.date_validation_with_hour_and_minutes(modified_date_string)
        modified_date = Parser.parse_event_date_from_string_input_with_hour_and_minutes(modified_date_string)
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
    """
    Metoda obsługuje funkcjonalność dodawania danych do kalendarza,
    przeprowadza walidację wprowadzonych danych oraz wyświetla odpowiednie informacje.

    Parameters:
        calendar (Calendar): obiekt klasy kalendarz.
    """

    # Pobranie daty wydarzenia i oczyszczenie terminalu.
    clear_terminal()
    event_date_str: str = (str(input('Podaj datę wydarzenia (YYYY-MM-DD-HH-MN) : ')))
    # Emulacja pętli do-while, służąca do walidacji wprowadzonej daty.
    date_validated: bool = Validator.date_validation_with_hour_and_minutes(event_date_str)
    while not date_validated:
        print_error('Podano niepoprawną datę!')
        input('Żeby podać ponownie, naciśnij enter : ')
        clear_terminal()
        event_date_str: str = (str(input('Podaj datę wydarzenia (YYYY-MM-DD-HH-MN) : ')))
        date_validated = Validator.date_validation_with_hour_and_minutes(event_date_str)
    # Ustalenie zwalidowanej daty.
    event_date: datetime = Parser.parse_event_date_from_string_input_with_hour_and_minutes(event_date_str)
    # Pobranie danych, bez potrzeby walidacji.
    description = str(input('Wprowadź opis zdarzenia : '))
    tag = str(input('Wprowadź tag zdarzenia (opcjonalne), wciśnij enter, jeżeli nie chcesz : '))
    # Dodanie danych do kalendarza, wraz z odpowiednim logiem.
    calendar.add_event(Event(event_date, description, tag))
    clear_terminal()
    print_log('Dodano wydarzenie do terminarza :)')
    input('Żeby wrócić do menu, naciśnij enter : ')


def handle_wrong_option() -> None:
    """
    Metoda wyświetla użytkownikowi podanie niepoprawnej opcji,
    prosząc o wciśnięcie klawisza enter, żeby przejść dalej.
    """

    print_error('Podano niepoprawną etykietę opcji!')
    input('Żeby wrócić, naciśnij enter : ')


def print_main_menu() -> None:
    """
    Metoda wyświetla dostępne w programie opcje.
    """

    print(Fore.LIGHTMAGENTA_EX + 'Dostępne opcje :' + Style.RESET_ALL)
    print('1. Dodaj wydarzenie do terminarza.')
    print('2. Modyfikuj wydarzenie z terminarza.')
    print('3. Usuń wydarzenie z terminarza.')
    print('4. Wylistuj wydarzenie z terminarza.')
    print('5. Zakończ pracę programu.')


def print_error(error_information: str) -> None:
    """
    Metoda wyświetla wyspecyfikowany błąd, zmieniając kolor na konsoli.

    Parameters:
          error_information (str): wyspecyfikowana informacja o błędzie.
    """

    print(Fore.LIGHTRED_EX + error_information + Style.RESET_ALL)


def print_log(log_information: str) -> None:
    """
    Metoda wyświetla wyspecyfikowany log, zmieniając kolor na konsoli.

    Parameters:
      log_information (str): wyspecyfikowany log.
    """

    print(Fore.LIGHTGREEN_EX + log_information + Style.RESET_ALL)


def print_info(info_information: str) -> None:
    """
    Metoda wyświetla wyspecyfikowaną informacje, zmieniając kolor na konsoli.

    Parameters:
        info_information (str): wyspecyfikowana informacja.
    """

    print(Fore.LIGHTMAGENTA_EX + info_information + Style.RESET_ALL)


def clear_terminal():
    """
    Metoda przeczyszcza terminal.
    """

    system('cls' if name == 'nt' else 'clear')


if __name__ == '__main__':
    main()
