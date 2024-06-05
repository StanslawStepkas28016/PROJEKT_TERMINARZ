from datetime import datetime


class Parser:
    @staticmethod
    def parse_event_date_from_string_input_with_hour_and_minutes(event_date_string: str) -> datetime:
        split = event_date_string.strip().split('-')

        return datetime(int(split[0]),
                        int(split[1]),
                        int(split[2]),
                        int(split[3]),
                        int(split[4]))

    @staticmethod
    def parse_event_date_from_string_input_without_hours_and_minutes(event_date_string: str) -> datetime:
        split = event_date_string.strip().split('-')

        return datetime(int(split[0]),
                        int(split[1]),
                        int(split[2]))
