import os
from datetime import datetime


class Validator:
    @staticmethod
    def date_validation_with_hour_and_minutes(event_date_string: str) -> bool:
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
        return os.stat('files/stored_state.txt').st_size == 0

    @staticmethod
    def does_calendar_file_exist() -> bool:
        return os.path.exists('files/stored_state.txt')
