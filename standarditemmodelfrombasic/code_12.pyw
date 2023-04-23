from PySide6.QtWidgets import (QTableView,
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

from listview_01 import ListView

class TableView(QTableView):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setDragDropMode(QTableView.DragDrop)
        self.setDefaultDropAction(Qt.MoveAction)

        self.standardItemModel = StandardItemModel()
        self.setModel(self.standardItemModel)

class StandardItemModel(QStandardItemModel):

    def __init__(self, parent=None):
        super().__init__(parent)

    def mimeTypes(self):

        return ['application/x-qabstractitemmodeldatalist',
                'application/x-qt-windows-mime;value=\"Shell IDList Array\"'
                ]

    def mimeData(self, indexes):

        qb = QByteArray()
        out = QDataStream(qb, QIODevice.WriteOnly)

        for index in indexes:
            item = self.itemFromIndex(index)
            out << item

        mimeData = QMimeData()
        mimeData.setData(
            self.mimeTypes()[0], qb
            )
        return mimeData

        
    def dropMimeData(self, data, action, row, column, parent):

        _row, _column = row, column

        if row == column == -1:
            row, column = parent.row(), parent.column()

        if row == column == -1:
            row = self.rowCount() -1
            
        if data.hasFormat(self.mimeTypes()[-1]):
            import random
            url = data.urls()[0]
            font = QFont("Arial", 72)
            icon = QIcon(url.toLocalFile())
            text = "item{}".format(self.rowCount())
            alignment = Qt.AlignLeft
            red = random.randint(0, 255)
            blue = random.randint(0, 255)
            green = random.randint(0, 255)
            foreground = QBrush(QColor(red, blue, green))
            red = random.randint(0, 255)
            blue = random.randint(0, 255)
            green = random.randint(0, 255)
            background = QBrush(QColor(red, blue, green))
            toolTip = "External Drop Neko"
            checkState = Qt.CheckState.Checked
            sizeHint = QSize(200, 200)
            item = QStandardItem()
            item.setFont(font)
            item.setIcon(icon)
            item.setText(text)
            item.setForeground(foreground)
            item.setBackground(background)
            item.setTextAlignment(alignment)
            item.setToolTip(toolTip)
            item.setCheckState(checkState)
            item.setSizeHint(sizeHint)
            self.appendRow(item)
            return False
            
        data = data.data(self.mimeTypes()[0])
        

        out = QDataStream(data, QIODevice.ReadOnly)

        while not out.atEnd():
            item = QStandardItem()
            out >> item

        if _row == _column == -1:
            row += 1            

        self.insertRow(row, item)

        if action == Qt.CopyAction:
            return False
        elif action == Qt.MoveAction:
            return True

        return True

def main():

    app = QApplication()
    w = QWidget()
    listView = ListView()
    tableView = TableView()
    h = QHBoxLayout()
    h.addWidget(listView)
    h.addWidget(tableView)
    w.setLayout(h)
    w.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
    
