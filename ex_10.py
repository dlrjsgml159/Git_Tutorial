import sys
import time
from threading import Timer

from PyQt5.QtWidgets import QApplication


class timer2():
    def showtime(self):
        print('sss')

        timer = Timer(1, self.showtime)
        timer.start()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = timer2()
    w.showtime()
    sys.exit(app.exec_())

