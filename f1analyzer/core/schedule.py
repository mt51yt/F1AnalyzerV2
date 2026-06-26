from datetime import datetime

from fastf1 import get_event_schedule, get_event
from fastf1.events import EventSchedule
from fastf1.logger import get_logger

from f1analyzer.config import START_YEAR

_logger = get_logger(__name__)

def get_all_years() -> list[str]:
    """
    :return: The list of years available.
    """
    return [str(i) for i in range(START_YEAR, datetime.today().year + 1)]

def get_all_year_rounds(year: int) -> EventSchedule:
    """
    :param year:
    :return: The list of rounds available for a given year.
    """
    event_schedule = get_event_schedule(year, include_testing=False)
    names = event_schedule[["EventName"]]
    return names

def get_all_round_sessions_names(year: int, rnd: int) -> list[str]:
    """
    :param year:
    :param rnd:
    :return: The list of sessions available for a given event.
    """
    event = get_event(year, rnd)
    session_names = [
        event[f'Session{i}']
        for i in range(1, 6)
        if event[f'Session{i}']
    ]

    return [name for name in session_names]