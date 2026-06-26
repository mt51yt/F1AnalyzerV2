from datetime import datetime
from pathlib import Path

from fastf1 import Cache, get_event_schedule, get_event
from fastf1 import get_session
from fastf1.core import Session
from fastf1.events import EventSchedule
from fastf1.logger import get_logger

_logger = get_logger(__name__)

START_YEAR: int = 2018
TESTING_EVENT_NAMES = {"Pre-Season Test", "Pre-Season Testing"}
SESSION_TYPE_MAP = {
    "P": ["Practice 1", "Practice 2", "Practice 3"],
    "Q": ["Qualifying", "Sprint Qualifying", "Sprint Shootout"],
    "R": ["Sprint", "Race"],
    "T": ["Practice 1", "Practice 2", "Practice 3"]
}

def load_session(year: int, gp: int | str, session: int | str,
                 load_laps: bool = False, load_telemetry: bool = False,
                 load_weather: bool = False, load_messages: bool = False) -> Session:
    """
    Used to load data from the specified session. You can demand to only load laps, telemetry, weather or messages.
    By default, it loads nothing to avoid loading data that is not needed. Warns if every boolean flag is false.

    :param year:
    :param gp:
    :param session:
    :param load_laps:
    :param load_telemetry:
    :param load_weather:
    :param load_messages:
    :return: The loaded session.
    """

    if None in (year, gp, session):
        raise ValueError("The year, grand prix and session must be provided.")

    if not (load_laps and load_telemetry and load_weather and load_messages):
        _logger.warning("No option were asked to be loaded.")

    cache_dir: str = str( Path(__file__).resolve().parents[2] / "cache" )
    Cache.enable_cache(cache_dir) #TODO: make a clean path for cache (especially update it in a config file)

    _session: Session = get_session(year, gp, session)
    _session.load(laps=load_laps, telemetry=load_telemetry,
                  weather=load_weather, messages=load_messages)

    return _session

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

def get_session_type_identifier(session: Session) -> str:
    """
    :param session:
    :return: The ID (P, Q, R) for a given session.
    """
    if session is None:
        raise ValueError("The session must be provided.")

    if not isinstance(session, Session):
        raise ValueError("The session must be a FastF1 Session.")

    if session.event["EventName"] in TESTING_EVENT_NAMES:
        return "T"

    for item in SESSION_TYPE_MAP.items():
        _id, names = item[0], item[1]
        if session.name in names:
            return _id

    raise ValueError(f"The session type {session.name} was not found.")