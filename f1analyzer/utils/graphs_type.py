from fastf1.core import Session
from f1analyzer.utils.load import get_session_type_identifier

ALL_GRAPHS: dict[str, list[str]] = {"PQ": ["axV", "ayV", "gg", "aeroSummary", "gapMap", "gapToFastest", "idealLap",
                                           "inputs", "miniSectorsMap", "predictedRacePace", "speedAcc", "speedDelta",
                                           "speedDeltaBattle", "vMin", "vMax", "loadFactor", "throttle", "vDifference"],

                                    "R":  ["dragReduction", "gapToWinner", "positionPerLap", "racePaceAnalysis",
                                           "raceStart", "raceStrategy", "minSpeedHeatMap", "maxSpeedHeatMap",
                                           "tyreDegFuelCorr"],

                                    "PR": ["tyreDegNoFuelCorr", "tyreWear"]}

# ID format XYY (X corresponds to PQ=1, R=2 or PR=3 and Y corresponds to the graph's number)
def get_id_graph_map() -> dict[int, str]:
    id_graph_map: dict[int, str] = {}
    for i, key in enumerate(ALL_GRAPHS):
        graphs: list[str] = ALL_GRAPHS[key]
        for j, graph in enumerate(graphs):
            id_graph_map[(i+1)*100 + (j+1)] = graph
    return id_graph_map

def get_available_graphs(session: Session) -> list[str]:
    session_identifier: str = get_session_type_identifier(session)

    if session_identifier == "P":
        return ALL_GRAPHS["PQ"] + ALL_GRAPHS["PR"]
    elif session_identifier == "Q":
        return ALL_GRAPHS["PQ"]
    else:
        return ALL_GRAPHS["R"] + ALL_GRAPHS["PR"]