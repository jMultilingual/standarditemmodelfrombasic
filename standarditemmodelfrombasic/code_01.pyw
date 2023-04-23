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
    listView.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
    
