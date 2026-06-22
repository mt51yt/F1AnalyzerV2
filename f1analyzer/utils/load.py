from pathlib import Path

import fastf1 as ff1
from fastf1.core import Session

def load_session(year: int, gp: int | str, session: int | str,
                 load_laps: bool = True, load_telemetry: bool = True,
                 load_weather: bool = False, load_messages: bool = False) -> Session | ValueError:

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
    ff1.Cache.enable_cache(cache_dir) #TODO: make a clean path for cache (especially update it in a config file)

    session: Session = ff1.get_session(year, gp, session)
    session.load(laps=load_laps, telemetry=load_telemetry,
                 weather=load_weather, messages=load_messages)

    return session

def get_session_type_identifier(session: Session) -> str:
    if session is None:
        raise ValueError("The session must be provided.")

    if not isinstance(session, Session):
        raise ValueError("The session must be a FastF1 Session.")

    if session.name == "Sprint" or session.name[0] == "R":
        return "R"
    elif "Practice" in session.name:
        return "P"
    else:
        return "Q"