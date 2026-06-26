from fastf1.core import Session, get_session
from fastf1.logger import get_logger

_logger = get_logger(__name__)

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

    _session: Session = get_session(year, gp, session)
    _session.load(laps=load_laps, telemetry=load_telemetry,
                  weather=load_weather, messages=load_messages)

    return _session

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