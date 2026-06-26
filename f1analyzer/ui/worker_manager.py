from PySide6.QtCore import QObject, QThread
from typing import cast
from f1analyzer.workers.session_loader import SessionLoaderWorker

class ThreadManager(QObject):

    def __init__(self, parent: QObject | None = None):
        super().__init__(parent)
        self._thread: QThread | None = None
        self._worker: QObject | None = None

    def load_session(self, year: int, gp: int | str, session: int | str,
                     on_success, on_error, on_progress=None):

        self._cancel_current()

        self._thread = QThread()
        assert self._thread is not None

        self._worker = SessionLoaderWorker(year, gp, session)
        worker = cast(SessionLoaderWorker, self._worker)

        worker.moveToThread(self._thread)

        self._thread.started.connect(worker.run)
        worker.finished.connect(on_success)
        worker.error.connect(on_error)
        if on_progress:
            worker.progress.connect(on_progress)

        worker.finished.connect(self._thread.quit)
        worker.error.connect(self._thread.quit)
        self._thread.finished.connect(self._thread.deleteLater)

        self._thread.start()

    def _cancel_current(self):
        if self._thread and self._thread.isRunning():
            self._thread.quit()
            self._thread.wait()