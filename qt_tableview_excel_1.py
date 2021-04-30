#!/usr/bin/env python
# coding: utf-8

# Reference:
# https://pc-technique.info/2020/02/207/

import pandas as pd
import sys
from typing import Any
from PySide2.QtCore import (
    Qt,
    QModelIndex,
    QAbstractTableModel
)

from PySide2.QtWidgets import (
    QApplication,
    QMainWindow,
    QTableView,
    QHeaderView,
)


class SimpleTableModel(QAbstractTableModel):
    def __init__(self, headers: list, source: list):
        QAbstractTableModel.__init__(self)
        self.headers = headers
        self.source = source

    # QVariant QAbstractItemModel::data(const QModelIndex &index, int role = Qt::DisplayRole) const
    def data(self, index: QModelIndex, role: int) -> Any:
        if role == Qt.DisplayRole:
            return self.source[index.row()][index.column()]

    def rowCount(self, parent=QModelIndex()) -> int:
        return len(self.source)

    def columnCount(self, parent=QModelIndex()) -> int:
        return len(self.headers)

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = Qt.DisplayRole):
        if role != Qt.DisplayRole:
            return
        if orientation == Qt.Horizontal:
            return self.headers[section]
        else:
            return "{}".format(section + 1)


class Example(QMainWindow):
    def __init__(self):
        super().__init__()

        # sample data
        filename = 'sample.xlsx'
        df = pd.read_excel(
            filename,
            engine='openpyxl',
        )

        self.initUI(df)
        self.setWindowTitle('TableView')
        self.show()

    def initUI(self, df):
        table: QTableView = QTableView()
        table.setWordWrap(False)
        table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

        # set table model
        headers = df.columns.values
        source = df.values.tolist()
        table.setModel(SimpleTableModel(headers, source))

        self.setCentralWidget(table)


def main():
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
