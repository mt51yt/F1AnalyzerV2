import pytest
from fastf1 import get_session
from f1analyzer.core.session import get_session_type_identifier
from test.build_test_cases import _build_test_cases

# Define the seasons and number of rounds we want to test
SEASONS = [2018, 2019, 2021, 2022, 2023, 2024, 2025, 2026]
SEASONS_ROUNDS = [21, 21, 22, 22, 22, 24, 24, 7]

# Define the correct mapping between id and name
ID_NAME_MATCHING: dict[str, str | list[str]] = {"P": ["Practice 1", "Practice 2", "Practice 3"],
                                                "Q": ["Qualifying", "Sprint Qualifying", "Sprint Shootout"],
                                                "R": ["Sprint", "Race"]}

TEST_CASES = _build_test_cases()

# Get the corresponding session with its id
def get_session_and_id(season, rnd, session):
    s = get_session(season, rnd, session)
    _id = get_session_type_identifier(s)
    return s, _id

# Test
@pytest.mark.parametrize("season,rnd,session",
                         TEST_CASES,
                         ids=[
                             f"{season}-R{rnd}-S{session}"
                             for season, rnd, session in TEST_CASES
                         ])
def test_compatibility(season: int, rnd: int, session: int):
    s, _id = get_session_and_id(season, rnd, session)
    assert s.name in ID_NAME_MATCHING[_id]