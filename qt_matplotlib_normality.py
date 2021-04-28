#!/usr/bin/env python
# coding: utf-8

from PySide2 import QtCore
from PySide2.QtCore import Qt
from PySide2 import QtGui
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
from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar,
)
import matplotlib.pyplot as plt
import pingouin as pg
from scipy.stats import (
    anderson,
    shapiro,
)
import seaborn as sns
import sys


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

        # Charts (center)
        charts = self.make_charts(data)
        self.setCentralWidget(charts)

        # Statistics (right dock)
        stats = self.make_stats(data)
        self.addDockWidget(Qt.RightDockWidgetArea, stats)

        # Toolbar
        self.addToolBar(
            QtCore.Qt.BottomToolBarArea,
            NavigationToolbar(charts, self)
        )

    def make_charts(self, data):
        sns.set_theme(style="whitegrid")

        fig = plt.figure(figsize=(5, 8))
        grid = fig.add_gridspec(12, 1)

        # ax
        ax1 = fig.add_subplot(grid[0:5, 0])
        # ax1.set_aspect(1)
        ax2 = fig.add_subplot(grid[6:7, 0])
        ax3 = fig.add_subplot(grid[8:11, 0])

        # Q-Q plot
        pg.qqplot(data, dist='norm', ax=ax1)
        # Boxplot
        sns.boxplot(x=data, ax=ax2)
        # Histogram
        sns.histplot(data, kde=True, ax=ax3)

        canvas = FigureCanvas(fig)
        return canvas

    def make_stats(self, data):
        dock = QDockWidget('Statistics')

        area = QScrollArea()
        area.setWidgetResizable(True)
        dock.setWidget(area)

        base = QWidget()
        base.setFont(QtGui.QFont("Helvetica [Cronyx]", 12))
        base.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        area.setWidget(base)

        grid = QGridLayout()
        grid.setHorizontalSpacing(0)
        grid.setVerticalSpacing(0)
        base.setLayout(grid)

        r = 0
        lab_gft = QLabel('Goodness of Fit Test')
        lab_gft.setFrameShape(QFrame.Panel)
        lab_gft.setFrameShadow(QFrame.Raised)
        grid.addWidget(lab_gft, r, 0, 1, 3)
        r += 1

        # ---------------------------------------------------------------------
        # Shapiro-Wilk
        r = self.tbl_shapiro_wilk_test(data, grid, r)

        # ---------------------------------------------------------------------
        # Anderson-Darling
        r = self.tbl_anderson_darling_test(data, grid, r)

        return dock

    def tbl_shapiro_wilk_test(self, data, grid, r):
        result_shapiro = shapiro(data)
        head_shapiro_1 = self.tbl_header_cell('W')
        grid.addWidget(head_shapiro_1, r, 1)
        head_shapiro_2 = self.tbl_header_cell('Prob &lt; W')
        grid.addWidget(head_shapiro_2, r, 2)
        r += 1

        lab_shapiro = self.tbl_row_header_cell('Shapiro-Wilk')
        grid.addWidget(lab_shapiro, r, 0)
        lab_shapiro_w = QLabel('{:.4f}'.format(result_shapiro.statistic))
        lab_shapiro_w.setAlignment(QtCore.Qt.AlignRight)
        lab_shapiro_w.setFrameShape(QFrame.Panel)
        lab_shapiro_w.setFrameShadow(QFrame.Sunken)
        grid.addWidget(lab_shapiro_w, r, 1)
        lab_shapiro_p = QLabel('{:.4f}'.format(result_shapiro.pvalue))
        lab_shapiro_p.setAlignment(QtCore.Qt.AlignRight)
        lab_shapiro_p.setFrameShape(QFrame.Panel)
        lab_shapiro_p.setFrameShadow(QFrame.Sunken)
        grid.addWidget(lab_shapiro_p, r, 2)
        r += 1

        return r

    def tbl_anderson_darling_test(self, data, grid, r):
        result_anderson = anderson(data)
        pvalue = self.calc_anderson_darling_probability(result_anderson.statistic, data.size)
        head_anderson_1 = self.tbl_header_cell('A<sup>2</sup>')
        grid.addWidget(head_anderson_1, r, 1)
        head_anderson_2 = self.tbl_header_cell('Prob &lt; A<sup>2</sup>')
        grid.addWidget(head_anderson_2, r, 2)
        r += 1

        lab_anderson = self.tbl_row_header_cell('Anderson-Darling')
        grid.addWidget(lab_anderson, r, 0)
        lab_anderson_a2 = QLabel('{:.4f}'.format(result_anderson.statistic))
        lab_anderson_a2.setAlignment(QtCore.Qt.AlignRight)
        lab_anderson_a2.setFrameShape(QFrame.Panel)
        lab_anderson_a2.setFrameShadow(QFrame.Sunken)
        grid.addWidget(lab_anderson_a2, r, 1)
        lab_anderson_p = QLabel('{:.4f}'.format(pvalue))
        lab_anderson_p.setAlignment(QtCore.Qt.AlignRight)
        lab_anderson_p.setFrameShape(QFrame.Panel)
        lab_anderson_p.setFrameShadow(QFrame.Sunken)
        grid.addWidget(lab_anderson_p, r, 2)
        r += 1

        return r

    def tbl_row_header_cell(self, str_label: str) -> QLabel:
        lab = QLabel(str_label)
        lab.setFrameShape(QFrame.Panel)
        lab.setFrameShadow(QFrame.Raised)

        return lab

    def tbl_header_cell(self, str_label: str) -> QLabel:
        lab = QLabel(str_label)
        lab.setAlignment(QtCore.Qt.AlignRight)
        lab.setFrameShape(QFrame.Panel)
        lab.setFrameShadow(QFrame.Raised)

        return lab

    def calc_anderson_darling_probability(self, ad, n):
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
