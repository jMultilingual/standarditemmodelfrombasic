from PySide6.QtWidgets import (QTreeView,
                               QWidget,
                               QHBoxLayout,
                               QStyledItemDelegate,
                               QApplication)
from PySide6.QtGui import (QStandardItemModel,
                           QStandardItem,
                           QIcon,
                           QFont,
                           QBrush,
                           QColor
                           )
from PySide6.QtCore import (Qt, QSaveFile, QSize, QDataStream,
                            QIODevice, QByteArray,
                            QMimeData, QFile,
                            QModelIndex)

import sys
import resources

from listview_05 import ListView
from tableview_01 import TableView

class TreeView(QTreeView):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setDragDropMode(QTreeView.DragDrop)
        self.setDefaultDropAction(Qt.MoveAction)
        self.setSelectionMode(QTreeView.ContiguousSelection)

        self.standardItemModel = StandardItemModel()
        self.setModel(self.standardItemModel)

class StandardItemModel(QStandardItemModel):

    def __init__(self, parent=None):
        super().__init__(parent)
        

def main():

    app = QApplication()

    listView = ListView()
    tableView = TableView()
    treeView = TreeView()
    w = QWidget()
    h = QHBoxLayout()
    h.addWidget(listView)
    h.addWidget(tableView)
    h.addWidget(treeView)
    w.setLayout(h)
    w.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
