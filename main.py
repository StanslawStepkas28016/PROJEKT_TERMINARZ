from datetime import date
from os import system, name
from time import sleep
from colorama import Fore, Back, Style
# to jest dodatkowy import dla paczki do kolorów tekstu wyświetlanego na konsoli

from utils_package.event import Event
from utils_package.calendar import Calendar
from utils_package.input_parser import Parser
from utils_package.input_validator import Validator


def main():
    print('**|** Projekt s28016 - Terminarz **|**')

    file_exists: bool = Calendar.does_calendar_file_exist()

    if file_exists:
        handle_old_user()
    else:
        handle_existing_user()


def handle_existing_user():
    print('Stwórz swój pierwszy terminarz!')
    calendar_name = str(input('Podaj nazwę swojego terminarza : '))
    calendar = Calendar(calendar_name)
    clear_terminal()

    print_main_menu()

    while True:
        option_etiquette = int(input('Wprowadź etykietę opcji : '))

        if option_etiquette > 4 or option_etiquette < 1:
            print('Podano niepoprawną etykietę opcji!')
            sleep(2)
        elif option_etiquette == 1:
            event_date: date = Parser.parse_event_date_from_input(str(input("Podaj datę zdarzenia (YYYY-MM-DD) : ")))
            description = str(input("Wprowadź opis zdarzenia : "))
            tag = str(input("Wprowadź tag zdarzenia (opcjonalne), wciśnij enter, jeżeli nie chcesz : "))
            calendar.add_event(Event(event_date, description, tag))
            print('Dodano wydarzenie do terminarza :)')
        elif option_etiquette == 2:
            events_list = calendar.get_events_sorted_by_date()

        clear_terminal()


def handle_old_user():
    print('None for now!')


def print_main_menu():
    print('Dostępne opcje :')
    print('1. Dodaj wydarzenie do terminarza.')
    print('2. Usuń wydarzenie z terminarza.')
    print('3. Wylistuj wydarzenie z terminarza.')
    print('4. Zakończ pracę programu.')


def clear_terminal():
    system('cls' if name == 'nt' else 'clear')


if __name__ == '__main__':
    main()
