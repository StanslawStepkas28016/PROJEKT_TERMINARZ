from datetime import date
from os import system, name
from time import sleep
from colorama import Fore, Back, Style
# to jest dodatkowy import dla paczki do kolorów tekstu wyświetlanego na konsoli

from utils_package.event import Event
from utils_package.calendar import Calendar
from utils_package.data_parser import Parser
from utils_package.data_validator import Validator


def main():
    print(Fore.LIGHTMAGENTA_EX + '*** Projekt s28016 - Terminarz ***' + Style.RESET_ALL)
    existing_user: bool = Calendar.does_calendar_file_exist()
    handle_user(existing_user)


def handle_user(existing_user: bool):
    calendar: Calendar = None

    if existing_user:
        calendar = Calendar.read_calendar_from_file_and_return_calendar_filled_with_events()
    else:
        print('Stwórz swój pierwszy terminarz!')
        calendar_name = str(input('Podaj nazwę swojego terminarza : '))
        calendar = Calendar(calendar_name)
        clear_terminal()

    while True:
        print_main_menu()
        option_etiquette = int(input('Wprowadź etykietę opcji : '))

        if option_etiquette > 4 or option_etiquette < 1:
            print(Fore.LIGHTRED_EX + 'Podano niepoprawną etykietę opcji!' + Style.RESET_ALL)
            sleep(1)
        elif option_etiquette == 1:
            # dodać walidację
            clear_terminal()
            event_date: date = Parser.parse_event_date_from_input(str(input("Podaj datę zdarzenia (YYYY-MM-DD) : ")))
            description = str(input("Wprowadź opis zdarzenia : "))
            tag = str(input("Wprowadź tag zdarzenia (opcjonalne), wciśnij enter, jeżeli nie chcesz : "))
            calendar.add_event(Event(event_date, description, tag))
            print('Dodano wydarzenie do terminarza :)')
        elif option_etiquette == 2:
            events_list = calendar.get_events_sorted_by_date()
            calendar.print_events_in_provided_list(events_list)
            event_index = int(input("Wprowadź numer zdarzenia do usunięcia : "))
            # walidacja etykiety na zasadzie, metoda sprawdza wartość, rzucając wyjątek.
            removed: bool = calendar.remove_event(event_index - 1)
            if not removed:
                print('Podano niepoprawny numer zdarzenia')
            else:
                print('Usunięto wydarzenie z terminarza')
        elif option_etiquette == 3:
            clear_terminal()
            print('Wydarzenia w terminarzu :')
            Calendar.print_events_in_provided_list(calendar.get_events_sorted_by_date())
            sleep(3)
        elif option_etiquette == 4:
            calendar.store_calendar_in_file()
            print('Kalendarz zapisany!')
            sleep(1)
            break

        clear_terminal()


def print_main_menu():
    print(Fore.LIGHTMAGENTA_EX + 'Dostępne opcje :' + Style.RESET_ALL)
    print('1. Dodaj wydarzenie do terminarza.')
    print('2. Usuń wydarzenie z terminarza.')
    print('3. Wylistuj wydarzenie z terminarza.')
    print('4. Zakończ pracę programu.')


def clear_terminal():
    system('cls' if name == 'nt' else 'clear')


if __name__ == '__main__':
    main()
