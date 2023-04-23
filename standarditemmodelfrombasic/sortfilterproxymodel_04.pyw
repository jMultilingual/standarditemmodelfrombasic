from PySide6.QtWidgets import (QApplication,
                               QWidget,
                               QTableView,
                               QGridLayout,
                               QLabel,
                               QLineEdit,
                               QSpinBox)

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

    def mousePressEvent(self, event):

        index = self.indexAt(event.position().toPoint())
        background = index.data(Qt.BackgroundRole)

        return super().mousePressEvent(event)

class LineEdit(QLineEdit):

    def __init__(self, model, spinbox, parent=None):

        super().__init__(parent)

        self.model = model
        self.spinbox = spinbox

    def setFilter(self, text):

        self.model.setFilterKeyColumn(
            self.spinbox.value()
            )
        self.model.setFilterRegularExpression(
            QRegularExpression(text)
            )
        
    
class SpinBox(QSpinBox):

    def __init__(self, model, parent=None):

        super().__init__(parent)
        self.setRange(0, 9)
        self.model = model

    def textFromValue(self, value):

        data = self.model.headerData(
            value, Qt.Horizontal
            )

        return data
        
            
    
def main():
    
    app = QApplication()
    standardModel = QStandardItemModel()
    standardView = QTableView()
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
    spinBox = SpinBox(proxyModel)
    lineEdit = LineEdit(proxyModel, spinBox)

    g.addWidget(standardLabel, 0, 0, 1, 1)
    g.addWidget(proxyLabel, 0, 1, 1, 1)
    g.addWidget(standardView, 1, 0, 1, 1)
    g.addWidget(proxyView, 1, 1, 1, 1)
    g.addWidget(spinBox, 2, 0, 1, 1)
    g.addWidget(lineEdit, 2, 1, 1, 1)

    proxyView.horizontalHeader().sectionPressed.connect(
            lambda index: proxyModel.sort(index,
                                proxyModel.sortOrder())
                )
    
    standardView.setModel(standardModel)   
    proxyModel.setSourceModel(standardModel)
    proxyView.setModel(proxyModel)
    lineEdit.textChanged.connect(lineEdit.setFilter)

    w.setLayout(g)  
    w.show()
    sys.exit(app.exec())           

if __name__ == "__main__":
    main()
