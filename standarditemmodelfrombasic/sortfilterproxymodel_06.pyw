from PySide6.QtWidgets import (QApplication,
                               QWidget,
                               QTreeView,
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
import os
    
class SortFilterProxyModel(QSortFilterProxyModel):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setAutoAcceptChildRows(True)
        self.setRecursiveFilteringEnabled(True)    

class TreeView(QTreeView):

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

        return str(data)

class StandardItem(QStandardItem):

    def __init__(self, _list, parent = None):
        super().__init__(parent)

        self.setText(_list[0])
        self._id = _list[1]
        self._wid = _list[2]
        self._pid = _list[3]
        self._turn = _list[4]
        self._isopen = _list[5]
        self._lid = _list[6]
        self._url = _list[7]
        self._keyboard = _list[8]
        self._font = _list[9]
        self._fontsize = _list[10]
    
class Dic(dict):

    def __missing__(self, key):

        return -1
    
def init_common_execution(cur, treeview, tablename="LANGUAGE", index=None):
    
    cur.execute(f"SELECT * FROM {tablename}")
    
    _all = cur.fetchall()
    model = treeview.model()
    dic = Dic({i[2]: StandardItem(list(i)) for i in _all})   

    model.layoutAboutToBeChanged.emit()
    values = dic.values()

    for v in values:

        if v is not None:
            
            order = int(v._turn)
            pid = v._pid
            if pid == '-1':
                pid = int(pid)
            if dic[pid] == -1:
                model.appendRow(v)
            else:
                parent = dic[pid]
                parent.setChild(order, v)
 
    model.layoutChanged.emit()
  

 
import sqlite3

def main():
    
    app = QApplication()
    standardModel = QStandardItemModel()
    standardView = QTreeView()
    proxyView = TreeView()
    proxyView.setSortingEnabled(True)
    proxyModel = SortFilterProxyModel()       
    
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
    
    standardView.setModel(standardModel)   
    proxyModel.setSourceModel(standardModel)
    proxyView.setModel(proxyModel)
    proxyView.header().sectionClicked.connect(
        lambda index: proxyModel.sort(index, Qt.AscendingOrder)
        )    
    lineEdit.textChanged.connect(lineEdit.setFilter)
 
    BASE_DIR = os.path.dirname(os.path.abspath(sys.argv[0]))
    db_path = os.path.join(BASE_DIR, "language_tree.db")
    with sqlite3.connect(db_path) as con:
        cur = con.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS LANGUAGE(NAME TEXT, ID TEXT, WID TEXT, PID TEXT, TURN INT, ISOPEN INT, LID TEXT PRIMARY KEY, URL TEXT , KEYBOARD TEXT, FONT TEXT, FONTSIZE INT)")
        init_common_execution(cur, standardView , "LANGUAGE")
    w.setLayout(g)  
    w.show()
    sys.exit(app.exec())           

if __name__ == "__main__":
    main()
