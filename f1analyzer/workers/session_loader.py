from PySide6.QtCore import QObject, Signal
from fastf1.core import Session
from f1analyzer.utils.load import load_session


class SessionLoaderWorker(QObject):

    finished = Signal(Session)
    error = Signal(str)
    progress = Signal(str)

    def __init__(self, year: int, gp: int | str, session: int | str):
        super().__init__()
        self._year = year
        self._gp = gp
        self._session = session

    def run(self):
        try:
            self.progress.emit(f"Loading {self._year} Round {self._gp} Session {self._session}...")
            session = load_session(self._year, self._gp, self._session)
            self.finished.emit(session)
        except Exception as e:
            self.error.emit(str(e))