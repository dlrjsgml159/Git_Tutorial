from PyQt5.QtWidgets import *
import sys

class CInputDialogWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUI()

    def setupUI(self):
        self.setWindowTitle("pyQtINputDialog")
        self.setGeometry(100,100,300,100)

        self.label = QLabel("age : ", self)
        self.label.move(20,20)
        self.label.resize(150,20)

        self.lineEdit = QLineEdit("",self)
        self.lineEdit.move(60,20)
        self.lineEdit.resize(200,20)
        self.lineEdit.setReadOnly(True)

        self.btnSave = QPushButton("number input", self)
        self.btnSave.move(10,50)
        self.btnSave.clicked.connect(self.btnInput_clicked)

    def btnInput_clicked(self):
        text, ok = QInputDialog.getInt(self, 'age', 'age input')

        if ok:
            self.lineEdit.setText(str(text))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CInputDialogWindow()
    window.show()
    app.exec_()

