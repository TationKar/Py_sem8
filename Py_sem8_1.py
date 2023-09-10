# Создать телефонный справочник с
# возможностью импорта и экспорта данных в
# формате .txt. Фамилия, имя, отчество, номер
# телефона - данные, которые должны находиться
# в файле.
# 1. Программа должна выводить данные
# 2. Программа должна сохранять данные в
# текстовом файле
# 3. Пользователь может ввести одну из
# характеристик для поиска определенной
# записи(Например имя или фамилию
# человека)
# 4. Использование функций. Ваша программа
# не должна быть линейной


# ВЕРСИЯ ДЛЯ QT

import sys
import json
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import *
from PyQt6.QtGui import QIcon, QStandardItem, QStandardItemModel
from random import randint
import AnotherWindow
from ui import Ui_MainWindow


def load():
    with open("contact.json", "r", encoding="utf-8") as fh:
        global phone_book
        phone_book = json.load(fh)
    print("Загрузка контактов выполнена успешно")


def save():
    with open("contact.json", "w", encoding="utf-8") as fh:
        fh.write(json.dumps(phone_book, ensure_ascii=False))
    print("Справочник сохранен")

tmp_phone = ""

try:
    load()
except:
    phone_book = [{"Дядя Петя": {"phone_numbers": [9998881234, 9997772233], "birth_day": "121276", "email": "mail@mail.ss"},
                   "Тетя Песя": {"phone_numbers": [9998881444]}}]
    save()


class AnotherWindow(QWidget):

    def __init__(self):
        super().__init__()

        global tmp_phone
        global phone_book
        is_red = False

        if (tmp_phone != ""):
            is_red = True
            temp_label = "Измените данные контакта"

            first_k = tmp_phone
            temp_dict = phone_book[tmp_phone]
            temp_num1 = temp_dict["phone_numbers"][0]

            try:
                temp_num2 = str(temp_dict["phone_numbers"][1])
            except:
                temp_num2 = ""

            try:
                red_b_day = temp_dict["birth_day"]
            except:
                red_b_day = ""
                
            try:
                red_mail = temp_dict["email"]
            except:
                red_mail = ""
            tmp_phone = ""
        else:
            temp_label = "Введите данные нового контакта"
        
        layout = QVBoxLayout()
        self.label = QLabel("Введите/измените данные контакта")
        layout.addWidget(self.label)
        self.line0 = QLineEdit()
        self.line0.setPlaceholderText("Введите имя")
        try:
            if is_red: 
                self.line0.setText(first_k)
                first_k = ""
        except:
            pass
        layout.addWidget(self.line0)
        self.line1 = QLineEdit()
        self.line1.setPlaceholderText("Введите номер тел.1")
        try:
            if is_red: 
                self.line1.setText(temp_num1)  
                temp_num1 = ""
        except:
            pass
        layout.addWidget(self.line1)
        self.line2 = QLineEdit()
        self.line2.setPlaceholderText("Введите номер тел.2")
        try:
            if is_red: 
                self.line2.setText(temp_num2)
                temp_num2 = ""
        except:
            pass
        layout.addWidget(self.line2)
        self.line3 = QLineEdit()
        self.line3.setPlaceholderText("Введите дату рождения")
        try:
            if is_red: 
                self.line3.setText(red_b_day)
                red_b_day = ""
        except:
            pass
        layout.addWidget(self.line3)
        self.line4 = QLineEdit()
        self.line4.setPlaceholderText("Введите email")
        try:
            if is_red: 
                self.line4.setText(red_mail)
                red_mail = ""
        except:
            pass
        layout.addWidget(self.line4)
        self.save_but = QtWidgets.QPushButton()
        self.save_but.setObjectName("sv_but")
        self.save_but.setText("Сохранить данные")
        layout.addWidget(self.save_but)
        self.setLayout(layout)
        self.save_but.clicked.connect(self.save_contact)
        tmp_phone == ""

    def save_contact(self):
        name_contact = self.line0.text()
        self.line0.clear()
        num_contact1 = self.line1.text()
        self.line1.clear()
        num_contact2 = self.line2.text()
        self.line2.clear()
        new_birth_day = self.line3.text()
        self.line3.clear()
        new_mail = self.line4.text()
        self.line4.clear()
        phone_book[name_contact] = {"phone_numbers": [
            num_contact1, num_contact2], "birth_day": new_birth_day, "email": new_mail}
        save()
        self.hide()


class Phone_bk(QtWidgets.QMainWindow):

    global tmp_phone

    def __init__(self):
        super(Phone_bk, self).__init__()
        
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.init_UI()
        # self.setup_connection()

    def init_UI(self):

        self.setWindowTitle('Телефонный справочник')
        self.ui.all_but.clicked.connect(self.fill_table)
        self.ui.add_but.clicked.connect(self.add_cont)
        self.ui.del_but.clicked.connect(self.del_contact)
        self.ui.red_but.clicked.connect(self.red_contact)
        self.ui.fnd_but.clicked.connect(self.fnd_contact)
        self.ui.hlp_but.clicked.connect(self.hlp_contact)
        self.ui.table_contacts.horizontalHeader().setStretchLastSection(True)
        self.model = QStandardItemModel()
        self.ui.table_contacts.setModel(self.model)

    def fill_table(self):

        model = self.ui.table_contacts.model()

        # Устанавливаем количество строк и столбцов в таблице
        model.setRowCount(len(phone_book))
        model.setColumnCount(4)

        row = 0
        temp_dict = {}
        for item_list in phone_book:
            temp_dict = phone_book[item_list]
            col = 0
            newitem = QStandardItem(item_list)
            model.setItem(row, col, newitem)
            for key in temp_dict:
                col += 1
                if str(type(temp_dict[key])) == "<class 'list'>":
                    temp_str = ', '.join(str(i) for i in temp_dict[key])
                    newitem = QStandardItem(temp_str)
                else:
                    newitem = QStandardItem(temp_dict[key])

                model.setItem(row, col, newitem)
            row += 1

        # Устанавливаем заголовки таблицы
        header_labels = ["Имя", "Телефоны", "Дата рождения", "E-mail"]
        for column in range(4):
            model.setHeaderData(
                column, Qt.Orientation.Horizontal, header_labels[column])

    def del_contact(self):
        name_delete, ok = QInputDialog.getText(
            self,
            "Удаление контакта",
            "Введите имя удаляемого контакта",
        )
        if ok:
            try:
                del phone_book[name_delete]
                dialog = QMessageBox(
                    parent=self, text=f"Контакт ''{name_delete}'' удален из списка")
                dialog.setWindowTitle("Delete Dialog")
            except:
                dialog = QMessageBox(
                    parent=self, text=f"Контакт ''{name_delete}'' отсутствует в списке, удаление возможно по полному имени")
                dialog.setWindowTitle("Delete Dialog")
            save()
            load()
            self.fill_table()

    def red_contact(self):
        global tmp_phone
        name_find_red, ok = QInputDialog.getText(
            self,
            "Поиск контакта",
            "Введите имя искомого контакта",
        )
        if ok:
            if name_find_red in phone_book:
                tmp_phone = name_find_red
                self.w = AnotherWindow()
                self.w.show()
                del phone_book[name_find_red]

    def fnd_contact(self):
        self.tmp_phone_book = {}

        name_find, ok = QInputDialog.getText(
            self,
            "Поиск контакта",
            "Введите имя искомого контакта",
        )

        if ok:
            not_found = True
            for contact in phone_book:
                if name_find in contact:
                    not_found = False
                    self.tmp_phone_book[contact] = phone_book[contact]

            if not_found == False:
                model = self.ui.table_contacts.model()

                # Устанавливаем количество строк и столбцов в таблице
                model.setRowCount(len(self.tmp_phone_book))
                model.setColumnCount(4)

                row = 0
                temp_dict = {}
                for item_list in self.tmp_phone_book:
                    temp_dict = self.tmp_phone_book[item_list]
                    col = 0
                    newitem = QStandardItem(item_list)
                    newitem.emitDataChanged()
                    model.setItem(row, col, newitem)
                    for key in temp_dict:
                        col += 1
                        if str(type(temp_dict[key])) == "<class 'list'>":
                            temp_str = ', '.join(str(i)
                                                 for i in temp_dict[key])
                            newitem = QStandardItem(temp_str)
                        else:
                            newitem = QStandardItem(temp_dict[key])
                            newitem.emitDataChanged()

                        model.setItem(row, col, newitem)
                    row += 1

                # Устанавливаем заголовки таблицы
                header_labels = ["Имя", "Телефоны", "Дата рождения", "E-mail"]
                for column in range(4):
                    model.setHeaderData(
                        column, Qt.Orientation.Horizontal, header_labels[column])

            if not_found:
                dialog = QMessageBox(
                    parent=self, text=f"Контакт ''{name_find}'' отсутствует в списке")
                dialog.setWindowTitle("Find Dialog")
                ret = dialog.exec()

            self.tmp_phone_book = {}

    def add_cont(self):
        self.w = AnotherWindow()
        self.w.show()

    def hlp_contact(self):
        dlg = QMessageBox(self)
        dlg.setWindowTitle("Краткая инструкция")
        dlg.setText("1. [Вывести список] - вывод списка всех контактов\n2. [Добавить контакт] - добавление контакта, заполните поля, после сохранения обновите список (см. 1 п.)\n3. [Удалить контакт] - введите полное имя\n4. [Изменить контакт] - введите полное имя, измените данные, сохраните и обновите список\n5. [Поиск контакта] - введите часть имени контакта, на экране останутся только подходящие контакты")
        button = dlg.exec()

        # if button == QMessageBox.StandardButton.Ok:
        #     print("OK!")


app = QtWidgets.QApplication([])
application = Phone_bk()
application.show()
save()
sys.exit(app.exec())
