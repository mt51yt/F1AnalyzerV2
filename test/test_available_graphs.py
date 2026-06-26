import pytest
from fastf1 import get_session

from f1analyzer.core.session import get_session_type_identifier
from f1analyzer.core.graphs_type import get_available_graphs
from test.build_test_cases import _build_test_cases

PRACTICE_GRAPHS: list[str] = ["axV", "ayV", "gg", "aeroSummary", "gapMap", "gapToFastest", "idealLap", "inputs",
                              "miniSectorsMap", "predictedRacePace", "speedAcc", "speedDelta", "speedDeltaBattle",
                              "vMin", "vMax", "loadFactor", "throttle", "vDifference", "tyreDegNoFuelCorr", "tyreWear"]

QUALIFYING_GRAPHS: list[str] = ["axV", "ayV", "gg", "aeroSummary", "gapMap", "gapToFastest", "idealLap", "inputs",
                                "miniSectorsMap", "predictedRacePace", "speedAcc", "speedDelta", "speedDeltaBattle",
                                "vMin", "vMax", "loadFactor", "throttle", "vDifference"]

RACE_GRAPHS: list[str] = ["dragReduction", "gapToWinner", "positionPerLap", "racePaceAnalysis", "raceStart",
                          "raceStrategy", "minSpeedHeatMap", "maxSpeedHeatMap", "tyreDegFuelCorr", "tyreDegNoFuelCorr",
                          "tyreWear"]

TEST_CASES = _build_test_cases()

# Test
@pytest.mark.parametrize("season,rnd,session",
                         TEST_CASES,
                         ids=[
                             f"{season}-R{rnd}-S{session}"
                             for season, rnd, session in TEST_CASES
                         ])
def test_available_graphs(season: int, rnd: int, session: int):
    s = get_session(season, rnd, session)
    graphs: list[str] = get_available_graphs(s)
    session_id = get_session_type_identifier(s)

    if session_id == "P":
        assert graphs == PRACTICE_GRAPHS
    elif session_id == "Q":
        assert graphs == QUALIFYING_GRAPHS
    elif session_id == "R":
        assert graphs == RACE_GRAPHS
    else:
        assert False, "Unknown session type"