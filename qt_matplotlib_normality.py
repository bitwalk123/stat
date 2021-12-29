#!/usr/bin/env python
# coding: utf-8

from PySide6 import QtCore
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
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
from matplotlib.backends.backend_qtagg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar,
)
import matplotlib.pyplot as plt
import math
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
        self.setFont(self.get_app_font())

        # sample dataset
        data = np.random.normal(loc=20, scale=5, size=100)

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
        base.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        area.setWidget(base)

        grid = QGridLayout()
        grid.setHorizontalSpacing(0)
        grid.setVerticalSpacing(0)
        base.setLayout(grid)

        r = 0
        lab_gft = self.tbl_section_title('Goodness of Fit Test')
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

        head_shapiro_1 = self.tbl_col_header_cell('W')
        grid.addWidget(head_shapiro_1, r, 1)
        head_shapiro_2 = self.tbl_col_header_cell('Prob &lt; W')
        grid.addWidget(head_shapiro_2, r, 2)
        r += 1

        lab_shapiro = self.tbl_row_header_cell('Shapiro-Wilk')
        grid.addWidget(lab_shapiro, r, 0)
        lab_shapiro_w = self.tbl_cell_value('{:.4f}'.format(result_shapiro.statistic))
        grid.addWidget(lab_shapiro_w, r, 1)
        lab_shapiro_p = self.tbl_cell_value('{:.4f}'.format(result_shapiro.pvalue))
        grid.addWidget(lab_shapiro_p, r, 2)
        r += 1

        return r

    def tbl_anderson_darling_test(self, data, grid, r):
        result_anderson = anderson(data)
        pvalue = self.calc_anderson_darling_probability(result_anderson.statistic, data.size)

        head_anderson_1 = self.tbl_col_header_cell('A<sup>2</sup>')
        grid.addWidget(head_anderson_1, r, 1)
        head_anderson_2 = self.tbl_col_header_cell('Prob &lt; A<sup>2</sup>')
        grid.addWidget(head_anderson_2, r, 2)
        r += 1

        lab_anderson = self.tbl_row_header_cell('Anderson-Darling')
        grid.addWidget(lab_anderson, r, 0)
        lab_anderson_a2 = self.tbl_cell_value('{:.4f}'.format(result_anderson.statistic))
        grid.addWidget(lab_anderson_a2, r, 1)
        lab_anderson_p = self.tbl_cell_value('{:.4f}'.format(pvalue))
        grid.addWidget(lab_anderson_p, r, 2)
        r += 1

        return r

    def tbl_section_title(self, title) -> QLabel:
        lab = QLabel(title)
        lab.setStyleSheet('QLabel {background-color: #028; color: #fff;}');
        lab.setFrameShape(QFrame.Panel)
        lab.setFrameShadow(QFrame.Raised)
        return lab

    def tbl_col_header_cell(self, title: str) -> QLabel:
        lab = QLabel(title)
        lab.setStyleSheet('QLabel {background-color: #ddf;}');
        lab.setAlignment(QtCore.Qt.AlignRight)
        lab.setFrameShape(QFrame.Panel)
        lab.setFrameShadow(QFrame.Raised)
        return lab

    def tbl_row_header_cell(self, title: str) -> QLabel:
        lab = QLabel(title)
        lab.setStyleSheet('QLabel {background-color: #ddf;}');
        lab.setFrameShape(QFrame.Panel)
        lab.setFrameShadow(QFrame.Raised)
        return lab

    def tbl_cell_value(self, value):
        lab = QLabel(value)
        lab.setStyleSheet('QLabel {background-color: #fff;}');
        lab.setAlignment(QtCore.Qt.AlignRight)
        lab.setFrameShape(QFrame.Panel)
        lab.setFrameShadow(QFrame.Sunken)
        return lab

    def get_app_font(self):
        font = QFont()
        font.setPointSize(12)
        font.setFixedPitch(True)
        return font

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
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
