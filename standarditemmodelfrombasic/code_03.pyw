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
        

def main():

    app = QApplication()

    listView = QListView()
    styledItemDelegate= StyledItemDelegate()
    listView.setItemDelegate(styledItemDelegate)
    
    standardItemModel = QStandardItemModel()
    listView.setModel(standardItemModel)

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
    standardItemModel.setItem(0, 0, item0)
    listView.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
    
    
