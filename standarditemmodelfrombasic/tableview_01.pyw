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

from listview_04 import ListView

class TableView(QTableView):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setDragDropMode(QTableView.DragDrop)
        self.setDefaultDropAction(Qt.MoveAction)

        self.standardItemModel = StandardItemModel()
        self.setModel(self.standardItemModel)
        self.setSelectionMode(QTableView.ContiguousSelection)

    def showEvent(self, event):
        self.load()
        return super().showEvent(event)

    def closeEvent(self, event):
        self.save()
        return super().closeEvent(event)        

    def save(self):

        file = QSaveFile("dummy_table.dat")
        if file.open(QIODevice.WriteOnly):
            out = QDataStream(file)
            model = self.model()
            rows = model.rowCount()
            cols = model.columnCount()
            out.writeUInt16(rows)
            out.writeUInt16(cols)
            for row in range(rows):
                for col in range(cols):

                    item = model.item(row, col)
                    if item is not None:
                        out.writeBool(True)
                    else:
                        out.writeBool(False)
                        continue
                    item.write(out)
            file.commit()

    def load(self):

        file = QFile("dummy_table.dat")
        if file.exists():
            if file.open(QIODevice.ReadOnly):
                out = QDataStream(file)
                rows = out.readUInt16()
                cols = out.readUInt16()
                model = self.model()
                model.clear()
                for row in range(rows):
                    for col in range(cols):
                        item = QStandardItem()
                        if not out.readBool():
                            continue
                        item.read(out)
                        model.setItem(row, col, item)
        file.close()
        

    def dropEvent(self, event):

        model = self.model()
        lastIndex = model.index(
            model.rowCount() - 1,
            model.columnCount() - 1,
            )
        rect = self.visualRect(lastIndex)
        global G_columnIsAboutToBeAdded
        G_columnIsAboutToBeAdded = False
        global G_rowIsAboutToBeAdded
        G_rowIsAboutToBeAdded = False
        global G_columnIsAboutToBeAddedCount
        G_columnIsAboutToBeAddedCount = 0
        global G_rowIsAboutToBeAddedCount
        G_rowIsAboutToBeAddedCount = 0
        
        if (model.rowCount() > 0
            and
            model.columnCount() > 0):

            if (rect.bottomRight().x() <
                event.position().toPoint().x()):
                

                G_columnIsAboutToBeAdded = True
                G_columnIsAboutToBeAddedCount = int((
                    
                event.position().toPoint().x() -

                rect.bottomRight().x())/ rect.width()
                                    ) + 1
            if (rect.bottomRight().y() <
                event.position().toPoint().y()):

                G_rowIsAboutToBeAdded = True
                G_rowIsAboutToBeAddedCount = int((

                event.position().toPoint().y() -
                rect.bottomRight().y())/ rect.height()
                ) + 1

        global G_probablyRow
        global G_probablyColumn

        rowPoint = event.position().toPoint()
        rowPoint.setX(0)
        columnPoint = event.position().toPoint()
        columnPoint.setY(0)
        G_probablyRow = self.indexAt(rowPoint).row()
        G_probablyColumn = self.indexAt(columnPoint).column()

        return super().dropEvent(event)
                                            

class StandardItemModel(QStandardItemModel):

    def __init__(self, parent=None):
        super().__init__(parent)

    def mimeTypes(self):

        return ['application/x-qabstractitemmodeldatalist',
                'application/x-qabstractitemmodeldatatable',
                'application/x-qt-windows-mime;value=\"Shell IDList Array\"'
                ]

    def mimeData(self, indexes):

        qb = QByteArray()
        out = QDataStream(qb, QIODevice.WriteOnly)
        startRow = indexes[0].row()
        startColumn = indexes[0].column()
        global G_endRow
        global G_endColumn
        G_endRow = 0
        G_endColumn = 0

        for index in indexes:
            item = self.item(index.row(), index.column())
            if item is None:
                out.writeBool(False)
                continue
            else:
                out.writeBool(True)
            out << item
            out.writeUInt16(index.row() - startRow)
            out.writeUInt16(index.column() - startColumn)

        G_endRow = index.row() - startRow
        G_endColumn = index.column() - startColumn
        
        mimeData = QMimeData()
        mimeData.setData(
            self.mimeTypes()[1], qb
            )
        
        return mimeData

    def setListMimeData(self, _row, _column, row, column, item, items):

        if row + len(items) > self.rowCount():
            global G_rowIsAboutToBeAdded
            global G_rowIsAboutToBeAddedCount
            G_rowIsAboutToBeAdded = True
            G_rowIsAboutToBeAddedCount = (row + len(items))\
                                            - (self.rowCount()
                                               )        
        if self.rowCount() == 0:
            for item in items:
                self.appendRow(item)

        elif G_rowIsAboutToBeAdded and G_columnIsAboutToBeAdded:
            self.setRowCount(
                self.rowCount() + G_rowIsAboutToBeAddedCount
                )
            self.setColumnCount(
                self.columnCount() + G_columnIsAboutToBeAddedCount
                )
            self.setItem(
                self.rowCount() -1, self.columnCount() - 1, item
                )

        elif G_rowIsAboutToBeAdded:

            self.setRowCount(
                self.rowCount() + G_rowIsAboutToBeAddedCount 
                )
            
            if len(items) > 1:
                
                for num, item in enumerate(items):
                    self.setItem(row + num, G_probablyColumn, item)
            else:
                
                self.setItem(
                    self.rowCount() - 1, G_probablyColumn, item
                    )

        elif G_columnIsAboutToBeAdded:
            self.setColumnCount(
                self.columnCount() + G_columnIsAboutToBeAddedCount
                )
            self.setItem(
                G_probablyRow, self.columnCount() - 1, item
                )
        elif _row == _column == -1:

            self.setItem(row, column, item)

    def setTableMimeData(self, _row, _column, row, column, item, items):

        if G_endRow + row > self.rowCount() - 1:
            global G_rowIsAboutToBeAdded
            global G_rowIsAboutToBeAddedCount
            G_rowIsAboutToBeAdded = True
            G_rowIsAboutToBeAddedCount = (G_endRow + row)\
                                         - (self.rowCount())

        if G_endColumn + column > self.columnCount() - 1:
            global G_columnIsAboutToBeAdded
            global G_columnIsAboutToBeAddedCount

            G_columnIsAboutToBeAdded = True
            G_columnIsAboutToBeAddedCount = (G_endColumn + column)\
                                            - (self.columnCount())

        if G_rowIsAboutToBeAdded and G_columnIsAboutToBeAdded:

            self.setRowCount(
                self.rowCount() + G_rowIsAboutToBeAddedCount
                )
            self.setColumnCount(
                self.columnCount() + G_columnIsAboutToBeAddedCount
                )
            for item in items:

                self.setItem(
                    row + item._relativeRow, column\
                    +item._relativeColumn, item
                    )
                del item._relativeRow
                del item._relativeColumn

        elif G_rowIsAboutToBeAdded:

            self.setRowCount(
                self.rowCount() + G_rowIsAboutToBeAddedCount
                )

            for item in items:

                self.setItem(
                    row + item._relativeRow, item._relativeColumn\
                    +column, item
                    )
                del item._relativeRow
                del item._relativeColumn

        elif G_columnIsAboutToBeAdded:

            self.setColumnCount(
                self.columnCount() + G_columnIsAboutToBeAddedCount
                )
            for item in items:

                self.setItem(
                    row + item._relativeRow, item._relativeColumn\
                    + column, item
                    )
                del item._relativeRow
                del item._relativeColumn

        elif _row == _column == -1:

            for item in items:

                self.setItem(
                    row + item._relativeRow, column\
                    + item._relativeColumn, item
                    )
                del item._relativeRow
                del item._relativeColumn
                
        
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

        elif data.hasFormat(self.mimeTypes()[1]):            
            
            data = data.data(self.mimeTypes()[1])
            out = QDataStream(data, QIODevice.ReadOnly)
            items = []
            while not out.atEnd():
                item = QStandardItem()
                if not out.readBool():
                    continue
                out >> item
                relativeRow = out.readUInt16()
                relativeColumn = out.readUInt16()
                item._relativeRow = relativeRow
                item._relativeColumn = relativeColumn                
                items.append(item)

            if len(items) == 1:
                self.setListMimeData(_row, _column, row, column, item, items)
            else:
                self.setTableMimeData(_row, _column, row, column, item, items)

        elif data.hasFormat(self.mimeTypes()[0]): 
        
            data = data.data(self.mimeTypes()[0])
            out = QDataStream(data, QIODevice.ReadOnly)
            items = []
            
            while not out.atEnd():
                item = QStandardItem()
                out >> item
                items.append(item)

            self.setListMimeData(_row, _column, row, column, item, items)           
                    

        if action == Qt.CopyAction:
            return False
        elif action == Qt.MoveAction:
            return True

        return True

class CloseWidget(QWidget):

    def __init__(self,  parent=None):
        super().__init__(parent)

    def closeEvent(self, event):

        for child in self.children():
            if isinstance(child, TableView):
                child.save()
        return super().closeEvent(event)    

def main():

    app = QApplication()
    w = CloseWidget()
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
    
