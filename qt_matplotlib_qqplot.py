#!/usr/bin/env python
# coding: utf-8

import sys
from PySide2 import QtCore
from PySide2.QtWidgets import (
    QApplication,
    QMainWindow,
)
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar,
)
import pingouin as pg


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.resize(500, 500)
        self.setWindowTitle('Q-Q plot on Qt5')
        self.show()

    def initUI(self):
        filename = 'data_norm.csv'
        data = np.loadtxt(filename, skiprows=1)

        fig = plt.figure(dpi=100)
        ax = fig.add_subplot(111)
        pg.qqplot(data, dist='norm', ax=ax)
        ax.set_title('example of Q-Q plot')
        canvas = FigureCanvas(fig)

        self.setCentralWidget(canvas)
        self.addToolBar(
            QtCore.Qt.BottomToolBarArea,
            NavigationToolbar(canvas, self)
        )


def main():
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
