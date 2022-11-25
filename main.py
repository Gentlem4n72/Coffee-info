import sys
import sqlite3

from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QDialog, QTableWidgetItem


class Coffee(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.connection = sqlite3.connect("coffee.sqlite")
        self.cursor = self.connection.cursor()
        self.show_table()

        self.pushButton.clicked.connect(self.add_sort)
        self.pushButton_2.clicked.connect(self.change_sort)

    def show_table(self):
        res = self.cursor.execute('''SELECT id, title,(SELECT title FROM roasting 
                                                                            WHERE id = roasting),
                                                                            (SELECT title FROM condition
                                                                            WHERE id = condition),
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

    def change_sort(self, item):
        dialog = addEditCoffeeForm()
        id = self.tableWidget.currentRow() + 1
        title, roasting, condition, discription, price, volume = (self.tableWidget.item(id - 1, 1).text(),
                                                                  self.tableWidget.item(id - 1, 2).text(),
                                                                  self.tableWidget.item(id - 1, 3).text(),
                                                                  self.tableWidget.item(id - 1, 4).text(),
                                                                  self.tableWidget.item(id - 1, 5).text(),
                                                                  self.tableWidget.item(id - 1, 6).text())
        dialog.lineEdit.setText(title)
        dialog.comboBox.setCurrentText(roasting)
        dialog.comboBox_2.setCurrentText(condition)
        dialog.lineEdit_2.setText(discription)
        dialog.lineEdit_3.setText(price)
        dialog.lineEdit_4.setText(volume)
        if dialog.exec():
            title, roasting, condition, discription, price, volume = (dialog.lineEdit.text(),
                                                                      dialog.comboBox.currentText(),
                                                                      dialog.comboBox_2.currentText(),
                                                                      dialog.lineEdit_2.text(),
                                                                      dialog.lineEdit_3.text(),
                                                                      dialog.lineEdit_4.text())
            self.cursor.execute('''UPDATE sorts
                                    SET title = ?, roasting = (SELECT id FROM roasting
                                                                WHERE title = ?),
                                                    condition = (SELECT id FROM condition
                                                                    WHERE title = ?),
                                                    discription = ?, price = ?, volume = ?
                                    WHERE id = ?''', (title, roasting, condition, discription, price, volume, id))
            self.connection.commit()
            self.show_table()

    def add_sort(self):
        dialog = addEditCoffeeForm()
        if dialog.exec():
            title, roasting, condition, discription, price, volume = (dialog.lineEdit.text(),
                                                                      dialog.comboBox.currentText(),
                                                                      dialog.comboBox_2.currentText(),
                                                                      dialog.lineEdit_2.text(),
                                                                      dialog.lineEdit_3.text(),
                                                                      dialog.lineEdit_4.text())
            self.cursor.execute('''INSERT INTO sorts(title, roasting, condition, discription, price, volume) 
                                    VALUES(?, (SELECT id FROM roasting
                                                WHERE title = ?),
                                                 (SELECT id FROM condition
                                                    WHERE title = ?), ?, ?, ?)''', (title, roasting, condition,
                                                                                    discription, price, volume))
            self.connection.commit()
            self.show_table()


class addEditCoffeeForm(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('addEditCoffeeForm.ui', self)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Coffee()
    ex.show()
    sys.exit(app.exec())
