import pytest
from fastf1 import get_session

from f1analyzer.utils.load import get_session_type_identifier
from f1analyzer.utils.graphs_type import get_available_graphs

PRACTICE_GRAPHS: list[str] = ["axV", "ayV", "gg", "aeroSummary", "gapMap", "gapToFastest", "idealLap", "inputs",
                              "miniSectorsMap", "predictedRacePace", "speedAcc", "speedDelta", "speedDeltaBattle",
                              "vMin", "vMax", "loadFactor", "throttle", "vDifference", "tyreDegNoFuelCorr", "tyreWear"]

QUALIFYING_GRAPHS: list[str] = ["axV", "ayV", "gg", "aeroSummary", "gapMap", "gapToFastest", "idealLap", "inputs",
                                "miniSectorsMap", "predictedRacePace", "speedAcc", "speedDelta", "speedDeltaBattle",
                                "vMin", "vMax", "loadFactor", "throttle", "vDifference"]

RACE_GRAPHS: list[str] = ["dragReduction", "gapToWinner", "positionPerLap", "racePaceAnalysis", "raceStart",
                          "raceStrategy", "minSpeedHeatMap", "maxSpeedHeatMap", "tyreDegFuelCorr", "tyreDegNoFuelCorr",
                          "tyreWear"]

# Define the seasons and number of rounds we want to test
SEASONS = [2018, 2019, 2021, 2022, 2023, 2024, 2025, 2026]
SEASONS_ROUNDS = [21, 21, 22, 22, 22, 24, 24, 7]

# Define all the test cases
TEST_CASES = [
    (season, rnd, session)
    for season, nb_rounds in zip(SEASONS, SEASONS_ROUNDS)
    for rnd in range(1, nb_rounds + 1)
    for session in range(1, 6)
]

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