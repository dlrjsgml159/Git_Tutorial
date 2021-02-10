from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sys

class CInputDialogWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUI()

    def setupUI(self):
        print("setupUI") #5
        self.setWindowTitle("PyQtInputDialog")
        self.setGeometry(100,100,300, 100)  #창이 뜰위치 창크기

        self.label = QLabel("과목 : " ,self)
        self.label.move(20,20)
        self.label.resize(150,20)

        self.lineEdit = QLineEdit("",self)
        self.lineEdit.move(60,20)
        self.lineEdit.resize(200,20)
        self.lineEdit.setReadOnly(True)

        self.btnSave = QPushButton("과목 선택 : ", self)
        self.btnSave.move(10,50)
        self.btnSave.clicked.connect(self.btnInput_clicked)

    def btnInput_clicked(self):
        print("btnInput_clicked")
        items = ("국어", "영어", "수학")
        item, ok = QInputDialog.getItem(self, "과목 선택", "과목을 선택하세요.", items,0 ,False)
        if ok and item:
            self.lineEdit.setText(item)

if __name__ == "__main__":
    print("if") #1
    app = QApplication(sys.argv) #2
    window = CInputDialogWindow() #3
    window.show() #4
    app.exec_()

print("end")


