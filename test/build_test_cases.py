from datetime import datetime
from f1analyzer.core.schedule import get_all_year_rounds

def _build_test_cases():
    cases = []
    for year in range(2018, datetime.today().year + 1):
        rounds = get_all_year_rounds(int(year))
        for rnd in rounds["RoundNumber"]:
            for session_num in range(1, 6):
                cases.append((int(year), int(rnd), session_num))
    return cases

TEST_CASES = _build_test_cases()