from datetime import datetime

import pyqtgraph as pg
import numpy as np

import RinfosDB

plt = pg.plot()
bufferSize = 1000
data = np.zeros(bufferSize)
curve = plt.plot()
line = plt.addLine(x=0)
plt.setRange(xRange=[0, bufferSize], yRange=[-50, 50])
i = 0


def update():
    db = RinfosDB.db()
    db.open('localhost')
    db.login('admin', 'admin')

    now = datetime.datetime.now()
    realtimes = now.today().strftime("%m/%d/%Y %H:%M")

    tiems, values = db.get_history('FLOW.P', '01/07/2021 14:07', realtimes)

    global data, curve, line, i
    n = 10  # update 10 samples per iteration
    rand = np.random.normal(size=n)
    data[i:i+n] = np.clip(data[i-1] + rand, -50, 50)
    curve.setData(data)
    i = (i+n) % bufferSize
    line.setValue(i)

timer = pg.QtCore.QTimer()
timer.timeout.connect(update)
timer.start(20)
pg.QtGui.QApplication.instance().exec_()