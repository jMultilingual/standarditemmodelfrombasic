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
import uuid

Qt.IdentifierRole = Qt.UserRole
Qt.ParentIdentifierRole = Qt.UserRole + 1

from listview_05 import ListView
from tableview_01 import TableView

class Dic(dict):

    def __missing__(self, key):

        return -1

class TreeView(QTreeView):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setDragDropMode(QTreeView.DragDrop)
        self.setDefaultDropAction(Qt.MoveAction)
        self.setSelectionMode(QTreeView.ContiguousSelection)

        self.standardItemModel = StandardItemModel()
        self.setModel(self.standardItemModel)

    def showEvent(self, event):
        self.load()
        return super().showEvent(event)
    
    def closeEvent(self, event):
        self.save()
        return super().closeEvent(event)
    
    def save(self):

        f = QSaveFile("dummy_tree.dat")
        if f.open(QIODevice.WriteOnly):

            out = QDataStream(f)
            model = self.model()

            for row in range(model.rowCount()):
                item = model.item(row, 0)
                self.recurWrite(item, out)

        f.commit()

    def recurWrite(self, item, out):

        item.write(out)
        out.writeQString(item._id)
        out.writeQString(item._pid)
        out.writeBool(self.isExpanded(item.index()))
        for c in range(item.rowCount()):
            child = item.child(c, 0)
            self.recurWrite(child, out)

    def load(self):

        dic = Dic()
        expanded = []
        f = QFile("dummy_tree.dat")
        if f.exists():
            if f.open(QIODevice.ReadOnly):

                out = QDataStream(f)
                while not out.atEnd():
                    treeitem = QStandardItem()
                    treeitem.read(out)
                    treeitem._id = out.readQString()
                    treeitem._pid = out.readQString()
                    treeitem._expanded = out.readBool()

                    dic[treeitem._id] = treeitem
                    if treeitem._expanded:
                        expanded.append(treeitem._id)

                    if dic[treeitem._pid] != -1:
                        dic[treeitem._pid].setChild(
                            dic[treeitem._pid].rowCount(),
                            0, treeitem
                            )
                    else:
                        self.model().appendRow(treeitem)
                for t in expanded:
                    if dic[t].index():
                        self.setExpanded(
                            dic[t].index(),
                            True
                            )
        f.close()

class StandardItemModel(QStandardItemModel):

    def __init__(self, parent=None):
        super().__init__(parent)

    def mimeTypes(self):

        return ['application/x-qabstractitemmodeldatalist',
                'application/x-qabstractitemmodeldatatable',
                'application/x-qabstractitemmodeldatatree',
                'application/x-qt-windows-mime;value=\"Shell IDList Array\"'
                ]


    def mimeData(self, indexes):

        qb = QByteArray()
        out = QDataStream(qb, QIODevice.WriteOnly)

        parentIndexes = (index for index in indexes
                         if index.parent() not in indexes)
        
        for index in indexes:
            
            self.writeMimeDataRecur(index, out)

        mimeData = QMimeData()
        mimeData.setData(
            self.mimeTypes()[2], qb
            )
        return mimeData

    def writeMimeDataRecur(self, index, out):

        item = self.itemFromIndex(index)
        out << item
        out.writeQString(item._id)
        out.writeQString(item._pid)
        if self.hasChildren(index):
            for r in range(self.rowCount(index)):
                child = self.index(r, 0, index)
                self.writeMimeDataRecur(child, out)
                

    def dropMimeData(self, data, action, row, column, parent):

        _row, _column = row, column

        if row == column == -1:
            row = parent.row()
            column = parent.column()

        if row == column == -1:
            row = self.rowCount() - 1
            
        dic = Dic()
        if data.hasFormat(self.mimeTypes()[2]):
            data = data.data(self.mimeTypes()[2])
            out = QDataStream(data, QIODevice.ReadOnly)
            while not out.atEnd():
                
                item = QStandardItem()
                out >> item
                item._id = out.readQString()
                item._pid = out.readQString()
                dic[item._id] = item
                
                if not parent.isValid():
                    self.setItem(self.rowCount(parent), item)

                elif _row == _column == -1:

                    if dic[item._pid] != -1:
                        parentItem = dic[item._pid]
                        parentItem.setChild(parentItem.rowCount(), 0, item)
                        item._pid = parentItem._id

                    else:
                        
                        parentItem = self.itemFromIndex(parent)
                        parentItem.setChild(parentItem.rowCount(), 0, item)
                        item._pid = parentItem._id
        
        elif data.hasFormat(self.mimeTypes()[1]):
            data = data.data(self.mimeTypes()[1])
            out = QDataStream(data, QIODevice.ReadOnly)

            while not out.atEnd():
                if not out.readBool():
                    continue
                
                item = QStandardItem()
                out >> item
                _ = out.readUInt16()
                _ = out.readUInt16()
                item._id = str(uuid.uuid4())
                item._pid = str(uuid.uuid4())
                if not parent.isValid():
                    self.setItem(self.rowCount(parent), item)

                elif _row == _column == -1:
                    parentItem = self.itemFromIndex(parent)
                    parentItem.setChild(parentItem.rowCount(), 0, item)
                    item._pid = parentitem._id
                    
        elif data.hasFormat(self.mimeTypes()[0]):
            data = data.data(self.mimeTypes()[0])
            out = QDataStream(data, QIODevice.ReadOnly)
            while not out.atEnd():

                item = QStandardItem()
                out >> item
                item._id = str(uuid.uuid4())
                item._pid = str(uuid.uuid4())

                if not parent.isValid():
                    self.setItem(self.rowCount(parent), item)

                elif _row == _column == -1:
                    parentItem = self.itemFromIndex(parent)
                    parentItem.setChild(parentItem.rowCount(), 0, item)
                    item._pid = parentItem._id
            
        if action == Qt.CopyAction:
            return False
        elif action == Qt.MoveAction:
            return True

        return False

class CloseWidget(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

    def closeEvent(self, event):

        for child in self.children():
            if isinstance(child, TreeView):
                child.save()

        return super().closeEvent(event)
    
def main():

    app = QApplication()

    listView = ListView()
    tableView = TableView()
    treeView = TreeView()
    w = CloseWidget()
    h = QHBoxLayout()
    h.addWidget(listView)
    h.addWidget(tableView)
    h.addWidget(treeView)
    w.setLayout(h)
    w.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
