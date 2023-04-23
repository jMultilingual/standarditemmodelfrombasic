from PySide6.QtWidgets import (QListView,
                               QStyledItemDelegate,
                               QApplication)

from PySide6.QtGui import (QStandardItemModel,
                           QStandardItem,
                           
                           QIcon,
                           QFont,
                           QBrush,
                           QColor
                           )
from PySide6.QtCore import (Qt, QSize, QDataStream,
                            QIODevice, QByteArray,
                            QMimeData, QFile, QSaveFile,
                            QModelIndex)

import sys
import resources

class StyledItemDelegate(QStyledItemDelegate):

    def __init__(self, parent=None):
        super().__init__(parent)

    def initStyleOption(self, option, index):
        super().initStyleOption(option, index)

        option.decorationSize = self.sizeHint(option, index)

        toolTip = index.data(Qt.ToolTipRole)
        if toolTip:
            option.toolTip = toolTip

    def paint(self, painter, option, index):

        return super().paint(painter, option, index)

    def sizeHint(self, option, index):

        return index.data(Qt.SizeHintRole)

    def createEditor(self, parent, option, index):

        editor = super().createEditor(parent, option, index)
        self.initStyleOption(option, index)
        editor.setFont(option.font)

        return editor

    def updateEditorGeometry(self, editor, option, index):

        editor.setGeometry(option.rect)

class ListView(QListView):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setDragDropMode(QListView.DragDrop)
        self.setDefaultDropAction(Qt.MoveAction)
        standardItemModel = StandardItemModel()
        self.setModel(standardItemModel)
        self.setItemDelegate(StyledItemDelegate())

class StandardItemModel(QStandardItemModel):

    def __init__(self, parent=None):
        super().__init__(parent)

        item0 = QStandardItem()
        item0.setText("item0")
        item0.setFont(QFont("Times New Roman", 18))
        item0.setIcon(QIcon(":/images/cat458A8400_TP_V4.jpg"))
        item0.setTextAlignment(Qt.AlignVCenter|Qt.AlignLeft)
        item0.setForeground(QBrush(QColor(105, 171, 197)))
        item0.setBackground(QBrush(QColor(237, 232, 159)))
        item0.setCheckState(Qt.CheckState.Checked)
        item0.setSizeHint(QSize(50, 50))
        item0.setFlags(item0.flags()|
                       Qt.ItemIsEditable|
                       Qt.ItemIsUserTristate)
        
        item1 = QStandardItem()
        item1.setText("item1")
        item1.setFont(QFont("Segoe UI Light", 36))
        item1.setIcon(QIcon(":/images/HIRAkotatuneko_TP_V4.jpg"))
        item1.setTextAlignment(Qt.AlignVCenter|Qt.AlignCenter)
        item1.setForeground(QBrush(QColor(246, 241, 214)))
        item1.setBackground(QBrush(QColor(117, 101,  93)))
        item1.setToolTip("Standard Model Neko1")
        item1.setCheckState(Qt.CheckState.PartiallyChecked)
        item1.setSizeHint(QSize(100, 100))
        item1.setFlags(item1.flags()|
                       Qt.ItemIsEditable|
                       Qt.ItemIsUserTristate)

        item2 = QStandardItem()
        item2.setText("item2")
        item2.setFont(QFont("Segoe UI Black", 72))
        item2.setIcon(QIcon(":/images/PPW_utatanewosuruneko_TP_V4.jpg"))
        item2.setTextAlignment(Qt.AlignVCenter|Qt.AlignRight)
        item2.setForeground(QBrush(QColor(176, 220, 213)))
        item2.setBackground(QBrush(QColor(213, 187, 216)))
        item2.setToolTip("Standard Model Neko2")
        item2.setCheckState(Qt.CheckState.Unchecked)
        item2.setSizeHint(QSize(150, 150))
        item2.setFlags(item2.flags()|
                       Qt.ItemIsEditable|
                       Qt.ItemIsUserTristate)

        self.appendRow(item0)
        self.appendRow(item1)
        self.appendRow(item2)

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
    listView = ListView()       
    listView.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
    
    
