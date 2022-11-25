import sys
import sqlite3

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QDialog, QTableWidgetItem


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(750, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(10, 520, 251, 31))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(490, 520, 251, 31))
        self.pushButton_2.setObjectName("pushButton_2")
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(10, 10, 731, 501))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 750, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "Добавить сорт"))
        self.pushButton_2.setText(_translate("MainWindow", "Изменить сорт"))


class Coffee(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.connection = sqlite3.connect("data/coffee.sqlite")
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
        if self.tableWidget.currentRow() != -1:
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


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(450, 230)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(10, 190, 431, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(10, 10, 111, 21))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(10, 40, 101, 21))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setGeometry(QtCore.QRect(10, 70, 101, 21))
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(Dialog)
        self.label_5.setGeometry(QtCore.QRect(10, 100, 101, 21))
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(Dialog)
        self.label_6.setGeometry(QtCore.QRect(10, 130, 101, 21))
        self.label_6.setObjectName("label_6")
        self.label_7 = QtWidgets.QLabel(Dialog)
        self.label_7.setGeometry(QtCore.QRect(10, 160, 101, 21))
        self.label_7.setObjectName("label_7")
        self.lineEdit = QtWidgets.QLineEdit(Dialog)
        self.lineEdit.setGeometry(QtCore.QRect(180, 10, 261, 20))
        self.lineEdit.setObjectName("lineEdit")
        self.comboBox = QtWidgets.QComboBox(Dialog)
        self.comboBox.setGeometry(QtCore.QRect(180, 40, 261, 22))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox_2 = QtWidgets.QComboBox(Dialog)
        self.comboBox_2.setGeometry(QtCore.QRect(180, 70, 261, 22))
        self.comboBox_2.setObjectName("comboBox_2")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.lineEdit_2 = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_2.setGeometry(QtCore.QRect(180, 100, 261, 20))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.lineEdit_3 = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_3.setGeometry(QtCore.QRect(180, 130, 261, 20))
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.lineEdit_4 = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_4.setGeometry(QtCore.QRect(180, 160, 261, 20))
        self.lineEdit_4.setObjectName("lineEdit_4")

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept) # type: ignore
        self.buttonBox.rejected.connect(Dialog.reject) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label_2.setText(_translate("Dialog", "Название:"))
        self.label_3.setText(_translate("Dialog", "Степень обжарки:"))
        self.label_4.setText(_translate("Dialog", "Молотый/Зерновой:"))
        self.label_5.setText(_translate("Dialog", "Описание вкуса:"))
        self.label_6.setText(_translate("Dialog", "Цена:"))
        self.label_7.setText(_translate("Dialog", "Объём упаковки:"))
        self.comboBox.setItemText(0, _translate("Dialog", "Легкая"))
        self.comboBox.setItemText(1, _translate("Dialog", "Средняя"))
        self.comboBox.setItemText(2, _translate("Dialog", "Сильная"))
        self.comboBox.setItemText(3, _translate("Dialog", "Экстремальная"))
        self.comboBox_2.setItemText(0, _translate("Dialog", "Молотый"))
        self.comboBox_2.setItemText(1, _translate("Dialog", "Зерновой"))


class addEditCoffeeForm(QDialog, Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Coffee()
    ex.show()
    sys.exit(app.exec())
