#!/usr/bin/env python
# coding: utf-8

import sys
from PySide2 import QtCore
from PySide2 import QtGui
from PySide2.QtCore import Qt
from PySide2.QtWidgets import (
    QApplication,
    QDockWidget,
    QFrame,
    QGridLayout,
    QLabel,
    QMainWindow,
    QScrollArea,
    QSizePolicy,
    QWidget,
)
import numpy as np
import math
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar,
)
import pingouin as pg
import seaborn as sns
from scipy.stats import (
    anderson,
    shapiro,
)


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.resize(800, 800)
        self.setWindowTitle('Normality Test on Qt5')
        self.show()

    def initUI(self):
        # sample dataset
        filename = 'data_norm.csv'
        data = np.loadtxt(filename, skiprows=1)

        sns.set_theme(style="whitegrid")
        fig = plt.figure(figsize=(5, 8))
        gs = fig.add_gridspec(12, 1)

        ax1 = fig.add_subplot(gs[0:5, 0])
        #ax1.set_aspect(1)
        ax2 = fig.add_subplot(gs[6:7, 0])
        ax3 = fig.add_subplot(gs[8:11, 0])

        # Q-Q plot
        a = pg.qqplot(data, dist='norm', ax=ax1)

        # Boxplot
        b = sns.boxplot(x=data, ax=ax2)

        # Histogram
        c = sns.histplot(data, kde=True, ax=ax3)

        # plt.show()
        canvas = FigureCanvas(fig)

        self.setCentralWidget(canvas)

        dock_stat = QDockWidget('Statistics')
        self.addDockWidget(Qt.RightDockWidgetArea, dock_stat)
        area = QScrollArea()
        area.setWidgetResizable(True)
        dock_stat.setWidget(area)

        base = QWidget()
        base.setFont(QtGui.QFont("Helvetica [Cronyx]", 12))
        base.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        area.setWidget(base)

        grid = QGridLayout()
        grid.setHorizontalSpacing(0)
        grid.setVerticalSpacing(0)
        base.setLayout(grid)

        r = 0
        label_gft = QLabel('Goodness of Fit Test')
        label_gft.setFrameShape(QFrame.Panel)
        label_gft.setFrameShadow(QFrame.Raised)
        grid.addWidget(label_gft, r, 0, 1, 3)
        r += 1

        # ---------------------------------------------------------------------
        # Shapiro-Wilk
        result_shapiro = shapiro(data)

        label_shapiro_h1 = self.make_header_cell('W')
        grid.addWidget(label_shapiro_h1, r, 1)
        label_shapiro_h2 = self.make_header_cell('Prob &lt; W')
        grid.addWidget(label_shapiro_h2, r, 2)
        r += 1

        label_shapiro = self.make_row_header_cell('Shapiro-Wilk')
        grid.addWidget(label_shapiro, r, 0)
        label_shapiro_w = QLabel('{:.4f}'.format(result_shapiro.statistic))
        label_shapiro_w.setAlignment(QtCore.Qt.AlignRight)
        label_shapiro_w.setFrameShape(QFrame.Panel)
        label_shapiro_w.setFrameShadow(QFrame.Sunken)
        grid.addWidget(label_shapiro_w, r, 1)
        label_shapiro_p = QLabel('{:.4f}'.format(result_shapiro.pvalue))
        label_shapiro_p.setAlignment(QtCore.Qt.AlignRight)
        label_shapiro_p.setFrameShape(QFrame.Panel)
        label_shapiro_p.setFrameShadow(QFrame.Sunken)
        grid.addWidget(label_shapiro_p, r, 2)
        r += 1

        # ---------------------------------------------------------------------
        # Anderson-Darling
        result_anderson = anderson(data)
        pvalue = self.calc_probability(result_anderson.statistic, data.size)

        label_anderson_h1 = self.make_header_cell('A<sup>2</sup>')
        grid.addWidget(label_anderson_h1, r, 1)
        label_anderson_h2 = self.make_header_cell('Prob &lt; A<sup>2</sup>')
        grid.addWidget(label_anderson_h2, r, 2)
        r += 1

        label_anderson = self.make_row_header_cell('Anderson-Darling')
        grid.addWidget(label_anderson, r, 0)
        label_anderson_w = QLabel('{:.4f}'.format(result_anderson.statistic))
        label_anderson_w.setAlignment(QtCore.Qt.AlignRight)
        label_anderson_w.setFrameShape(QFrame.Panel)
        label_anderson_w.setFrameShadow(QFrame.Sunken)
        grid.addWidget(label_anderson_w, r, 1)
        label_anderson_p = QLabel('{:.4f}'.format(pvalue))
        label_anderson_p.setAlignment(QtCore.Qt.AlignRight)
        label_anderson_p.setFrameShape(QFrame.Panel)
        label_anderson_p.setFrameShadow(QFrame.Sunken)
        grid.addWidget(label_anderson_p, r, 2)
        r += 1

        self.addToolBar(
            QtCore.Qt.BottomToolBarArea,
            NavigationToolbar(canvas, self)
        )

    def make_row_header_cell(self, str_label:str) -> QLabel:
        lab = QLabel(str_label)
        lab.setFrameShape(QFrame.Panel)
        lab.setFrameShadow(QFrame.Raised)
        return lab

    def make_header_cell(self, str_label:str) -> QLabel:
        lab = QLabel(str_label)
        lab.setAlignment(QtCore.Qt.AlignRight)
        lab.setFrameShape(QFrame.Panel)
        lab.setFrameShadow(QFrame.Raised)
        return lab

    def calc_probability(self, ad, n):
        ad_adj = ad * (1 + (0.75 / n) + 2.25 / (n ** 2))
        if ad_adj >= 0.6:
            prob = math.exp(1.2937 - 5.709 * ad_adj - 0.0186 * (ad_adj ** 2))
        elif ad_adj >= 0.34:
            prob = math.exp(0.9177 - 4.279 * ad_adj - 1.38 * (ad_adj ** 2))
        elif ad_adj > 0.2:
            prob = 1 - math.exp(-8.318 + 42.796 * ad_adj - 59.938 * (ad_adj ** 2))
        else:
            prob = 1 - math.exp(-13.436 + 101.14 * ad_adj - 223.73 * (ad_adj ** 2))
        return prob


def main():
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
