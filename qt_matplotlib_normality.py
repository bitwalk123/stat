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
import seaborn as sns



class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.resize(500, 800)
        self.setWindowTitle('Normality on Qt5')
        self.show()

    def initUI(self):
        # sample dataset
        filename = 'data_norm.csv'
        data = np.loadtxt(filename, skiprows=1)

        sns.set_theme(style="whitegrid")
        fig = plt.figure(figsize=(5, 10))
        gs = fig.add_gridspec(12, 1)

        ax1 = fig.add_subplot(gs[0:5, 0])
        ax2 = fig.add_subplot(gs[6:7, 0])
        ax3 = fig.add_subplot(gs[8:11, 0])

        # Q-Q plot
        a = pg.qqplot(data, dist='norm', ax=ax1)

        # Boxplot
        b = sns.boxplot(x=data, ax=ax2)

        # Histogram
        c = sns.histplot(data, kde=True, ax=ax3)

        #plt.show()
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
