from PySide6.QtCore import QAbstractItemModel, QModelIndex, QObject, Qt
from PySide6.QtWidgets import QTreeView, QDockWidget
from enum import Enum, auto

from f1analyzer.utils.load import get_all_year_rounds, get_all_round_sessions_names, get_all_years


class NodeType(Enum):
    ROOT = auto()
    YEAR = auto()
    ROUND = auto()
    SESSION = auto()


class SessionTreeNode:

    def __init__(self, data: dict, node_type: NodeType, parent=None) -> None:
        self.data = data
        self.node_type = node_type
        self.parent_node = parent
        self.children: list[SessionTreeNode] = []
        self.children_loaded: bool = False

    def child(self, row: int) -> "SessionTreeNode":
        return self.children[row]

    def child_count(self) -> int:
        return len(self.children)

    def row(self) -> int:
        if self.parent_node:
            return self.parent_node.children.index(self)
        return 0

    def display_text(self) -> str:
        match self.node_type:
            case NodeType.ROOT: return 'root'
            case NodeType.YEAR: return f'{self.data['year']}'
            case NodeType.ROUND: return f'{self.data['round']}'
            case NodeType.SESSION: return f'{self.data['session']}'


class SessionTreeModel(QAbstractItemModel):

    def __init__(self, years: list[str], parent: QObject | None = None) -> None:
        super().__init__(parent)

        self._root = SessionTreeNode(data={}, node_type=NodeType.ROOT, parent=parent)

        for year in sorted(years, reverse=True):
            node = SessionTreeNode(
                data={"year": year},
                node_type=NodeType.YEAR,
                parent=self._root
            )
            self._root.children.append(node)

    def index(self, row: int, column: int, parent: QModelIndex = QModelIndex()) -> QModelIndex:
        if not self.hasIndex(row, column, parent):
            return QModelIndex()

        parent_node = self._node_from_index(parent)
        assert parent_node is not None
        child_node = parent_node.child(row)

        if child_node:
            return self.createIndex(row, column, child_node)
        return QModelIndex()

    def parent(self, index: QModelIndex = QModelIndex()) -> QModelIndex:
        if not index.isValid():
            return QModelIndex()

        child_node = self._node_from_index(index)
        assert child_node is not None
        parent_node = child_node.parent_node

        # If parent is root, return invalid index (root has no visual parent)
        if parent_node is self._root:
            return QModelIndex()

        return self.createIndex(parent_node.row(), 0, parent_node)

    def rowCount(self, parent: QModelIndex = QModelIndex()) -> int:
        node = self._node_from_index(parent)
        assert node is not None
        return node.child_count()

    def columnCount(self, parent: QModelIndex = QModelIndex()) -> int:
        return 1

    def data(self, index: QModelIndex, role: int = Qt.ItemDataRole.DisplayRole) -> str | None:
        if not index.isValid():
            return None
        if role == Qt.ItemDataRole.DisplayRole:
            node = self._node_from_index(index)
            assert node is not None
            return node.display_text()
        return None

    def hasChildren(self, parent: QModelIndex = QModelIndex()) -> bool:
        node = self._node_from_index(parent)
        if node is None:
            return False

        if node.node_type == NodeType.SESSION:
            return False

        if node.node_type == NodeType.ROOT or node.children_loaded:
            return node.child_count() > 0

        return True

    def _node_from_index(self, index: QModelIndex) -> SessionTreeNode | None:
        if index.isValid():
            return index.internalPointer()
        return self._root

    def _find_year_node(self, year: int) -> SessionTreeNode | None:
        for child in self._root.children:
            if child.data["year"] == year:
                return child
        return None

    def _find_round_node(self, year: int, round_num: int) -> SessionTreeNode | None:
        year_node = self._find_year_node(year)
        assert year_node is not None
        for child in year_node.children:
            if child.data["round"] == round_num:
                return child
        return None

    def canFetchMore(self, parent: QModelIndex) -> bool:
        if not parent.isValid():
            return False
        node = self._node_from_index(parent)

        assert node is not None
        if node.node_type == NodeType.SESSION:
            return False
        return not node.children_loaded

    def fetchMore(self, parent: QModelIndex) -> None:
        node = self._node_from_index(parent)
        assert node is not None

        # Fetch the right level of data depending on node type
        if node.node_type == NodeType.YEAR:
            children = self._fetch_rounds(node.data["year"])
        elif node.node_type == NodeType.ROUND:
            children = self._fetch_sessions(node.data["year"], node.data["round"])
        else:
            return

        self.beginInsertRows(parent, 0, len(children) - 1)
        node.children = children
        node.children_loaded = True
        self.endInsertRows()

    def _fetch_rounds(self, year: int) -> list[SessionTreeNode]:
        raw = get_all_year_rounds(int(year))
        parent_node = self._find_year_node(year)

        return [
            SessionTreeNode(
                data={"year": year, "round": raw.iloc[i, 0]},
                node_type=NodeType.ROUND,
                parent=parent_node
            )
            for i in range(len(raw))
        ]

    def _fetch_sessions(self, year: int, rnd: int) -> list[SessionTreeNode]:
        raw = get_all_round_sessions_names(int(year), rnd)
        parent_node = self._find_round_node(year, rnd)
        return [
            SessionTreeNode(
                data={"year": year, "round": rnd, "session": s},
                node_type=NodeType.SESSION,
                parent=parent_node
            )
            for s in raw
        ]


class SessionExplorer(QDockWidget):

    def __init__(self, parent=None):
        super().__init__("Session Explorer", parent)

        years: list[str] = get_all_years()
        model: SessionTreeModel = SessionTreeModel(years)

        self.tree = QTreeView()
        self.tree.setModel(model)
        self.tree.setHeaderHidden(True)

        self.setFeatures(QDockWidget.DockWidgetFeature.NoDockWidgetFeatures)
        self.setAllowedAreas(Qt.DockWidgetArea.LeftDockWidgetArea)

        self.setWidget(self.tree)