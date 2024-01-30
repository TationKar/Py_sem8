""" Реализовать консольное приложение заметки, с сохранением, чтением,
 добавлением, редактированием и удалением заметок. Заметка должна
содержать идентификатор, заголовок, тело заметки и дату/время создания или
последнего изменения заметки. Сохранение заметок необходимо сделать в
формате json или csv формат (разделение полей рекомендуется делать через
точку с запятой). Реализацию пользовательского интерфейса студент может
делать как ему удобнее, можно делать как параметры запуска программы
(команда, данные), можно делать как запрос команды с консоли и
последующим вводом данных, как-то ещё, на усмотрение студента.
Например 
python notes.py add --title "новая заметка" –msg "тело новой заметки"
Или так:
python note.py
Введите команду: add
Введите заголовок заметки: новая заметка
Введите тело заметки: тело новой заметки
Заметка успешно сохранена
Введите команду:
При чтении списка заметок реализовать фильтрацию по дате."""


# ВЕРСИЯ ДЛЯ QT

from datetime import date
import datetime
import sys
import json
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import Qt, QSortFilterProxyModel
from PyQt6.QtWidgets import *
from PyQt6.QtGui import QIcon, QStandardItem, QStandardItemModel
from random import randint
import AnotherWindow
from ui import Ui_MainWindow


def load():
    with open("contact.json", "r", encoding="utf-8") as fh:
        global note_book
        note_book = json.load(fh)
    print("Загрузка заметок выполнена успешно")


def save():
    with open("contact.json", "w", encoding="utf-8") as fh:
        fh.write(json.dumps(note_book, ensure_ascii=False))
    print("Справочник сохранен")

tmp_note = ""

try:
    load()
except:
    note_book = {"First_note_ID": {"date_note": "","name_note": "Первая заметка", "text_note": "Это первая заметка в приложении"}, "Second_note_ID": {"date_note": "","name_note": "Вторая заметка", "text_note": "Текст второй заметки"}}
    save()

class AnotherWindow(QWidget):

    def __init__(self):
        super().__init__()

        global tmp_note
        global note_book
        is_red = False

        if (tmp_note != ""):
            is_red = True
            temp_label = "Измените данные"

            first_k = tmp_note
            temp_dict = note_book[tmp_note]
            temp_num1 = temp_dict["name_note"]

            try:
                red_b_day = temp_dict["text_note"]
            except:
                red_b_day = ""
                
            try:
                red_date = temp_dict["date_note"]
            except:
                red_date = ""
            tmp_note = ""
        else:
            temp_label = "Введите данные заметки"
        
        layout = QVBoxLayout()
        self.label = QLabel("Введите/измените данные заметки")
        layout.addWidget(self.label)
        self.line0 = QLineEdit()
        self.line0.setPlaceholderText("Введите идентификатор")
        try:
            if is_red: 
                self.line0.setText(first_k)
                first_k = ""
        except:
            pass
        layout.addWidget(self.line0)

        self.line1 = QLineEdit()
        txtdate = datetime.datetime.now().strftime("%d-%m-%Y %H:%M")
        self.line1.setPlaceholderText(txtdate)
        try:
            if is_red: 
                self.line1.setText(txtdate)
                red_date = ""
        except:
            pass
        self.line1.setText(txtdate)
        layout.addWidget(self.line1)

        self.line3 = QLineEdit()
        self.line3.setPlaceholderText("Введите заголовок")
        try:
            if is_red: 
                self.line3.setText(temp_num1)  
                temp_num1 = ""
        except:
            pass
        layout.addWidget(self.line3)

        self.line4 = QLineEdit()
        self.line4.setPlaceholderText("Введите заметку")
        try:
            if is_red: 
                self.line4.setText(red_b_day)
                red_b_day = ""
        except:
            pass
        layout.addWidget(self.line4)

        self.save_but = QtWidgets.QPushButton()
        self.save_but.setObjectName("sv_but")
        self.save_but.setText("Сохранить данные")
        layout.addWidget(self.save_but)
        self.setLayout(layout)
        self.save_but.clicked.connect(self.save_contact)
        tmp_note == ""

    def save_contact(self):
        name_contact = self.line0.text()
        self.line0.clear()
        num_contact1 = self.line1.text()
        self.line1.clear()
        new_text_note = self.line3.text()
        self.line3.clear()
        new_mail = self.line4.text()
        self.line4.clear()
        note_book[name_contact] = {"date_note": num_contact1, "name_note": 
            new_text_note, "text_note": new_mail}
        save()

        self.hide()


class Phone_bk(QtWidgets.QMainWindow):

    global tmp_note

    def __init__(self):
        super(Phone_bk, self).__init__()
        
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.init_UI()

    def init_UI(self):

        self.setWindowTitle('Хранение заметок')
        self.ui.all_but.clicked.connect(self.fill_table)
        self.ui.add_but.clicked.connect(self.add_cont)
        self.ui.del_but.clicked.connect(self.del_contact)
        self.ui.red_but.clicked.connect(self.red_contact)
        self.ui.fnd_but.clicked.connect(self.fnd_note)
        self.ui.fnd_but_2.clicked.connect(self.fnd_date)
        self.ui.hlp_but.clicked.connect(self.hlp_contact)
        self.ui.table_contacts.horizontalHeader().setStretchLastSection(True)
        self.model = QStandardItemModel()
        self.ui.table_contacts.setModel(self.model)
        

    def fill_table(self):

        model = self.ui.table_contacts.model()

        # Устанавливаем количество строк и столбцов в таблице
        model.setRowCount(len(note_book))
        model.setColumnCount(4)

        row = 0
        temp_dict = {}
        for item_list in note_book:
            temp_dict = note_book[item_list]
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
        header_labels = ["Идентификатор", "Дата", "Заголовок", "Заметка"]
        for column in range(4):
            model.setHeaderData(
                column, Qt.Orientation.Horizontal, header_labels[column])

    def del_contact(self):
        name_delete, ok = QInputDialog.getText(
            self,
            "Удаление заметки",
            "Введите идентификатор",
        )
        if ok:
            try:
                del note_book[name_delete]
                dialog = QMessageBox(
                    parent=self, text=f"Заметка ''{name_delete}'' удалена из списка")
                dialog.setWindowTitle("Delete Dialog")
            except:
                dialog = QMessageBox(
                    parent=self, text=f"Заметка ''{name_delete}'' отсутствует в списке, удаление возможно по полному имени")
                dialog.setWindowTitle("Delete Dialog")
            save()
            load()
            self.fill_table()

    def red_contact(self):
        global tmp_note
        name_find_red, ok = QInputDialog.getText(
            self,
            "Поиск заметки",
            "Введите идентификатор",
        )
        if ok:
            if name_find_red in note_book:
                tmp_note = name_find_red
                self.w = AnotherWindow()
                self.w.show()
                del note_book[name_find_red]

    def fnd_note(self):
        self.tmp_note_book = {}

        name_find, ok = QInputDialog.getText(
            self,
            "Поиск заметки",
            "Введите идентификатор",
        )

        if ok:
            not_found = True
            for contact in note_book:
                if name_find in contact:
                    not_found = False
                    self.tmp_note_book[contact] = note_book[contact]

            if not_found == False:
                model = self.ui.table_contacts.model()

                # Устанавливаем количество строк и столбцов в таблице
                model.setRowCount(len(self.tmp_note_book))
                model.setColumnCount(4)

                row = 0
                temp_dict = {}
                for item_list in self.tmp_note_book:
                    temp_dict = self.tmp_note_book[item_list]
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
                header_labels = ["Идентификатор", "Дата", "Заголовок", "Заметка"]
                for column in range(4):
                    model.setHeaderData(
                        column, Qt.Orientation.Horizontal, header_labels[column])

            if not_found:
                dialog = QMessageBox(
                    parent=self, text=f"Заметка ''{name_find}'' отсутствует в списке")
                dialog.setWindowTitle("Find Dialog")
                ret = dialog.exec()

            self.tmp_note_book = {}





    def fnd_date(self):
        self.tmp_note_book = {}

        date_find, ok = QInputDialog.getText(
            self,
            "Поиск заметки",
            "Введите дату",
        )

        if ok:
            not_found = True
            for contact in note_book:
                tmpDct = note_book[contact]
                tempStr = tmpDct["date_note"]
                if date_find in tempStr:
                    not_found = False
                    self.tmp_note_book[contact] = note_book[contact]

            if not_found == False:
                model = self.ui.table_contacts.model()

                # Устанавливаем количество строк и столбцов в таблице
                model.setRowCount(len(self.tmp_note_book))
                model.setColumnCount(4)

                row = 0
                temp_dict = {}
                for item_list in self.tmp_note_book:
                    temp_dict = self.tmp_note_book[item_list]
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
                header_labels = ["Идентификатор", "Дата", "Заголовок", "Заметка"]
                for column in range(4):
                    model.setHeaderData(
                        column, Qt.Orientation.Horizontal, header_labels[column])

            if not_found:
                dialog = QMessageBox(
                    parent=self, text=f"Заметка ''{name_find}'' отсутствует в списке")
                dialog.setWindowTitle("Find Dialog")
                ret = dialog.exec()

            self.tmp_note_book = {}

    def add_cont(self):
        self.w = AnotherWindow()
        self.w.show()

    def hlp_contact(self):
        dlg = QMessageBox(self)
        dlg.setWindowTitle("Краткая инструкция")
        dlg.setText("1. [Вывести список] - вывод списка всех заметок\n2. [Добавить заметку] - добавление заметки, заполните поля, после сохранения обновите список (см. 1 п.)\n3. [Удалить заметку] - введите полное имя\n4. [Изменить заметку] - введите полное имя, измените данные, сохраните и обновите список\n5. [Поиск заметки] - введите часть имени заметки, на экране останутся только подходящие\n6. [Фильтр по дате] - введите часть даты заметки(ок), на экране останутся только подходящие")
        button = dlg.exec()


app = QtWidgets.QApplication([])
application = Phone_bk()
application.show()
save()
sys.exit(app.exec())
