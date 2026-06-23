from datetime import datetime
from pathlib import Path

from fastf1 import Cache
from fastf1 import get_session
from fastf1.core import Session
from fastf1.logger import get_logger

_logger = get_logger(__name__)

START_YEAR: int = 2018
YEAR_RND_MAP: dict[int, int] = {2018: 21, 2019: 21, 2020: 17, 2021: 22, 2022: 22,
                                2023: 22, 2024: 24, 2025: 24, 2026: 22}
SESSION_TYPE_MAP = {
    "P": ["Practice 1", "Practice 2", "Practice 3"],
    "Q": ["Qualifying", "Sprint Qualifying", "Sprint Shootout"],
    "R": ["Sprint", "Race"],
}

def load_session(year: int, gp: int | str, session: int | str,
                 load_laps: bool = True, load_telemetry: bool = True,
                 load_weather: bool = False, load_messages: bool = False) -> Session:

    """
    Used to load data from the specified session. You can demand to only load laps, telemetry, weather or messages.
    By default, it loads only laps and telemetry.

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

    cache_dir: str = str( Path(__file__).resolve().parents[2] / "cache" )
    Cache.enable_cache(cache_dir) #TODO: make a clean path for cache (especially update it in a config file)

    session: Session = get_session(year, gp, session)
    session.load(laps=load_laps, telemetry=load_telemetry,
                 weather=load_weather, messages=load_messages)

    return session

def get_all_sessions() -> list[Session]:
    all_sessions: list[Session] | None = loop_all_sessions(datetime.today())
    assert all_sessions is not None, "No sessions found."

    return all_sessions

def loop_all_sessions(date: datetime) -> list[Session] | None:
    all_sessions: list[Session] = []
    for year in range(START_YEAR, date.year + 1):
        for rnd in range(1, YEAR_RND_MAP[year] + 1):
            for s_num in range(1, 6):
                try:
                    s = get_session(year, rnd, s_num)
                    if s.date > date:
                        return all_sessions
                    all_sessions.append(s)
                except ValueError:  
                    _logger.warning(f"Session {s_num} for round {rnd} of year {year} was not found.")

    return None

def get_session_type_identifier(session: Session) -> str:
    if session is None:
        raise ValueError("The session must be provided.")

    if not isinstance(session, Session):
        raise ValueError("The session must be a FastF1 Session.")

    for item in SESSION_TYPE_MAP.items():
        _id, names = item[0], item[1]
        if session.name in names:
            return _id

    raise ValueError(f"The session type {session.name} was not found.")