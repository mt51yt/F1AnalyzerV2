from fastf1.core import Session
from f1analyzer.core.session import get_session_type_identifier

ALL_GRAPHS: dict[str, list[str]] = {"PQ": ["axV", "ayV", "gg", "aeroSummary", "gapMap", "gapToFastest", "idealLap",
                                           "inputs", "miniSectorsMap", "predictedRacePace", "speedAcc", "speedDelta",
                                           "speedDeltaBattle", "vMin", "vMax", "loadFactor", "throttle", "vDifference"],

                                    "R":  ["dragReduction", "gapToWinner", "positionPerLap", "racePaceAnalysis",
                                           "raceStart", "raceStrategy", "minSpeedHeatMap", "maxSpeedHeatMap",
                                           "tyreDegFuelCorr"],

                                    "PR": ["tyreDegNoFuelCorr", "tyreWear"]}

def get_available_graphs(session: Session) -> list[str]:
    """
    Get the graphs that can be plotted for a given session type.

    :param session:
    :return: A list of the available graphs names.
    """
    session_identifier: str = get_session_type_identifier(session)

    if session_identifier == "P":
        return ALL_GRAPHS["PQ"] + ALL_GRAPHS["PR"]
    elif session_identifier == "Q":
        return ALL_GRAPHS["PQ"]
    else:
        return ALL_GRAPHS["R"] + ALL_GRAPHS["PR"]