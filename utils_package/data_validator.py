import os
from datetime import datetime


class Validator:
    """
    Klasa służy do walidacji danych, nad którymi pracuje program.
    """

    @staticmethod
    def date_validation_with_hour_and_minutes(event_date_string: str) -> bool:
        """
        Metoda sprawdza, czy podana przez użytkownika data jest rzeczywiście datą,
        w formacie 'YYYY-MM-DD-HH-MM'.

        Parameters:
            event_date_string (str): string zawierający podaną dane w formacie 'YYYY-MM-DD-HH-MM'.

        Returns:
            bool: typ bool, który potwierdza, lub zaprzecza,
            jakoby podana przez użytkownika data, była datą w określonym formacie.
        """
        date_split: list[str] = event_date_string.split('-')
        try:
            datetime(int(date_split[0]),
                     int(date_split[1]),
                     int(date_split[2]),
                     int(date_split[3]),
                     int(date_split[4]))
        except (ValueError, IndexError):
            return False
        else:
            return True

    @staticmethod
    def date_validation_without_hours_and_minutes(event_date_string: str) -> bool:
        """
        Metoda sprawdza, czy podana przez użytkownika data jest rzeczywiście datą,
        w formacie 'YYYY-MM-DD'.

        Parameters:
            event_date_string (str): string zawierający podaną dane w formacie 'YYYY-MM-DD'.

        Returns:
            bool: typ bool, który potwierdza, lub zaprzecza,
            jakoby podana przez użytkownika data, była datą w określonym formacie.
        """
        date_split: list[str] = event_date_string.split('-')
        try:
            datetime(int(date_split[0]),
                     int(date_split[1]),
                     int(date_split[2]))
        except (ValueError, IndexError):
            return False
        else:
            return True

    @staticmethod
    def is_calendar_file_empty() -> bool:
        """
        Metoda sprawdza, czy plik, służący do przechowywania
        zapisanych danych z kalendarza jest pusty.

        Returns:
            bool: typ bool, który potwierdza, lub zaprzecza,
            jakoby plik był pusty.
        """
        return os.stat('files/stored_state.txt').st_size == 0

    @staticmethod
    def does_calendar_file_exist() -> bool:
        """
        Metoda sprawdza, czy plik, służący do przechowywania
        zapisanych danych z kalendarza istnieje.

        Returns:
            bool: typ bool, który potwierdza, lub zaprzecza,
            jakoby plik istniał.
        """
        return os.path.exists('files/stored_state.txt')
