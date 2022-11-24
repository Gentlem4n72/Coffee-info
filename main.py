import sys
import sqlite3

from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidgetItem


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.connection = sqlite3.connect("coffee.sqlite")
        res = self.connection.cursor().execute('''SELECT id, title,(SELECT title FROM roasting_degrees 
                                                                    WHERE degree_id = roasting),
                                                                    (SELECT title FROM conditions
                                                                    WHERE condition_id = condition),
                                                                    discription,
                                                                    price,
                                                                    volume
                                                                    FROM sorts''').fetchall()
        self.tableWidget.setColumnCount(7)
        self.tableWidget.setRowCount(0)
        self.tableWidget.setHorizontalHeaderLabels(('ID', 'Название', 'Степень обжарки', 'Молотый/Зерновой',
                                                    'Описание вкуса', 'Цена', 'Объём упаковки'))
        horizontal_h = self.tableWidget.horizontalHeader()
        horizontal_h.resizeSection(0, 30)
        horizontal_h.resizeSection(1, 80)
        horizontal_h.resizeSection(2, 110)
        horizontal_h.resizeSection(3, 125)
        horizontal_h.resizeSection(4, 220)
        horizontal_h.resizeSection(5, 40)
        horizontal_h.resizeSection(6, 100)

        for i, row in enumerate(res):
            self.tableWidget.setRowCount(
                self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(
                    i, j, QTableWidgetItem(str(elem)))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())
