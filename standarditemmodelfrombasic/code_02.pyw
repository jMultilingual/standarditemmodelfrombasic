from PySide6.QtWidgets import (QListView,
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

def main():

    app = QApplication()

    listView = QListView()
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
    
    
