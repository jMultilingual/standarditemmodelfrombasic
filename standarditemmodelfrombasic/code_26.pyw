from PySide6.QtWidgets import (QApplication,
                               QWidget,
                               QTableView,
                               QGridLayout,
                               QLabel)

from PySide6.QtGui import (QIcon, QFont, QBrush, QColor,
                           QStandardItemModel, QStandardItem)

from PySide6.QtCore import (QSize, Qt, QSaveFile,
                            QFile, QIODevice, QDataStream,
                            QByteArray, QMimeData,
                            QSortFilterProxyModel,
                            QRegularExpression)
import sys, csv
import resources

class SortFilterProxyModel(QSortFilterProxyModel):

    def __init__(self, parent=None):

        super().__init__(parent) 


class TableView(QTableView):

    def __init__(self, parent=None):
        super().__init__(parent)
    
   
def main():
    
    app = QApplication()
    standardModel = QStandardItemModel()
    standardView = TableView()
    proxyView = TableView()
    proxyModel = SortFilterProxyModel()

    with open("dummy.cgi") as csvfile:
        
        dummyreader = csv.reader(csvfile, delimiter=',')
        data = [r for r in dummyreader]

        standardModel.setHorizontalHeaderLabels(
                                data.pop(0)
                                )      
        standardItems = [
            
            [QStandardItem(d) for d in c]
            
            for c in data]

        for row, standardItem in enumerate(standardItems):
            for col, d in enumerate(standardItem):
                standardModel.setItem(row, col, d)         
    
    w = QWidget()
    g = QGridLayout()

    standardLabel = QLabel("スタンダードモデル")
    proxyLabel = QLabel("プロキシモデル")

    g.addWidget(standardLabel, 0, 0, 1, 1)
    g.addWidget(proxyLabel, 0, 1, 1, 1)
    g.addWidget(standardView, 1, 0, 1, 1)
    g.addWidget(proxyView, 1, 1, 1, 1)

    proxyView.horizontalHeader().sectionPressed.connect(
                lambda index: proxyModel.sort(index,
                                        proxyModel.sortOrder())
                )
    
    standardView.setModel(standardModel)   
    proxyModel.setSortRole(Qt.BackgroundRole)
    proxyModel.setSourceModel(standardModel)
    proxyView.setModel(proxyModel)

    w.setLayout(g)  
    w.show()
    sys.exit(app.exec())           

if __name__ == "__main__":
    main()
