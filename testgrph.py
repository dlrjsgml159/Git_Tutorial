import sys
from threading import Timer

from PyQt5.QtWidgets import QApplication
import pyqtgraph as pg
import numpy as np
import datetime
import RinfosDB


class Trandes():
    def init(self):
        self.db = RinfosDB.db()
        self.db.open('localhost')
        self.db.login('admin', 'admin')

        self.now = datetime.datetime.now()
        self.realtimes = self.now.today().strftime("%m/%d/%Y %H:%M")

        self.tiems, self.values = self.db.get_history('FLOW.P', '01/07/2021 14:07', self.realtimes)

        self.y = np.array(self.values)
        print(self.y)
        self.x = np.arange(self.y.size)
        print(self.x)
        self.plotWidget = pg.plot(title="Three plot curves")

        for i in range(1):
            self.plotWidget.plot(self.x, self.y, pen=(i, 3))


        self.adddata()

    def adddata(self):
        onevalue = self.db.get('FLOW.P')
        print(onevalue)
        self.plotWidget.setData(self.x, self.y)

        self.timer = Timer(1, self.adddata)
        self.timer.daemon = True
        self.timer.start()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    trande = Trandes()

    trande.init()

    status = app.exec_()
    sys.exit(status)