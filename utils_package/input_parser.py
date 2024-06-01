from datetime import date


class Parser:
    @staticmethod
    def parse_event_date_from_input(event_date_string: str) -> date:
        split = event_date_string.split("-")
        return date(int(split[0]), int(split[1]), int(split[2]))
