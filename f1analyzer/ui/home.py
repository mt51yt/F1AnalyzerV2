from PySide6.QtCore import Qt
from PySide6.QtGui import QAction, QIcon
from PySide6.QtWidgets import QApplication, QMainWindow, QToolBar, QWidget, QVBoxLayout, QMenuBar, QMenu, QDockWidget, QMessageBox

from fastf1.core import Session

from f1analyzer.ui.widgets.session_explorer import SessionExplorer


class Home(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("F1 Analyzer V2 - Home")

        ico: QIcon = QIcon("img/ico.png")
        self.setWindowIcon(ico)

        self._build_menubar()
        self._build_toolbars()
        self._build_graph_viz()

    def _build_menubar(self):
        menubar: QMenuBar | None = self.menuBar()
        assert menubar is not None

        file_menu: QMenu | None = menubar.addMenu("&File")
        assert file_menu is not None

        file_menu.addAction(QAction("New", self))
        file_menu.addAction(QAction("Open…", self))
        file_menu.addSeparator()
        quit_action: QAction = QAction("Quit", self)
        quit_action.triggered.connect(self.close)
        file_menu.addAction(quit_action)

        help_menu: QMenu | None = menubar.addMenu("&Help")
        assert help_menu is not None

        help_menu.addAction(QAction("About", self))
        #TODO: update menubar when new ideas and functionalities come up

    def _build_explorer(self):
        self.explorer: QDockWidget = SessionExplorer(self)
        self.addDockWidget(
            Qt.DockWidgetArea.LeftDockWidgetArea,
            self.explorer
        )

    def _build_available_graphs(self):
        available_graphs: QToolBar = QToolBar("Available Graphs")
        available_graphs.setMovable(False)

        self.addToolBar(Qt.ToolBarArea.RightToolBarArea, available_graphs)

        #TODO: add a checkable list of the available graphs from defined constants

    def _build_graphs_options(self):
        graphs_options: QToolBar = QToolBar("Graphs Options")
        graphs_options.setMovable(False)

        self.addToolBar(Qt.ToolBarArea.BottomToolBarArea, graphs_options)

        #TODO: get options for the displayed graphs and display it on this toolbox (if no options say so)

    def _build_toolbars(self):
        self._build_explorer()
        self._build_available_graphs()
        self._build_graphs_options()

    def _build_graph_viz(self):
        graph_viz: QWidget = QWidget()
        _ = QVBoxLayout(graph_viz)

        self.setCentralWidget(graph_viz)

    def _on_session_loaded(self, session: Session):
        self._set_loading_state(False)
        self._current_session = session
        #self._refresh_graph_panel()

    def _on_load_error(self, message: str):
        self._set_loading_state(False)
        # Show an error dialog or status bar message
        QMessageBox.critical(self, "Load Error", message)

    def _on_progress(self, message: str):
        self.statusBar().showMessage(message)

    def _set_loading_state(self, loading: bool):
        # Disable the session explorer while loading to prevent re-entrant calls
        self.explorer.setEnabled(not loading)