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

    def dropMimeData(self, data, action, row, column, parent):

        _row, _column = row, column

        if row == column == -1:
            row = parent.row()
            column = parent.column()

        if row == column == -1:
            row = self.rowCount() - 1

        data = data.data(self.mimeTypes()[0])
        out = QDataStream(data, QIODevice.ReadOnly)
        while not out.atEnd():

            item = QStandardItem()
            out >> item

            if not parent.isValid():
                self.setItem(self.rowCount(parent), item)

            elif _row == _column == -1:
                parentItem = self.itemFromIndex(parent)
                parentItem.setChild(parentItem.rowCount(), 0, item)
            
        if action == Qt.CopyAction:
            return False
        elif action == Qt.MoveAction:
            return True

        return False
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
