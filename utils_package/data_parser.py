from datetime import datetime

"""
Klasa, która pozwala na zamianę wartości typu string,
na obiekty typu datetime.
"""


def parse_event_date_from_string_input_with_hour_and_minutes(event_date_string: str) -> datetime:
    """
    Metoda fabrykuje nowy obiekt klasy datetime, na podstawie wejściowych danych
    typu string. Zwracany obiekt jest w formacie 'YYYY-MM-DD-HH-MM'.

    Parameters:
        event_date_string (str): string zawierający datę w formacie 'YYYY-MM-DD-HH-MM'.

    Returns:
        date_time: obiekt klasy datetime, zawierający datę w formacie 'YYYY-MM-DD-HH-MM'.
    """

    split = event_date_string.strip().split('-')

    return datetime(int(split[0]),
                    int(split[1]),
                    int(split[2]),
                    int(split[3]),
                    int(split[4]))


def parse_event_date_from_string_input_without_hours_and_minutes(event_date_string: str) -> datetime:
    """
    Metoda fabrykuje nowy obiekt klasy datetime, na podstawie wejściowych danych
    typu string. Zwracany obiekt jest w formacie 'YYYY-MM-DD'.

    Parameters:
        event_date_string (str): string zawierający datę w formacie 'YYYY-MM-DD'.

    Returns:
        date_time: obiekt klasy datetime, zawierający datę w formacie 'YYYY-MM-DD'.
    """

    split = event_date_string.strip().split('-')

    return datetime(int(split[0]),
                    int(split[1]),
                    int(split[2]))
