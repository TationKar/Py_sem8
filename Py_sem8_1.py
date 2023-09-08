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
    

try:
    load()
except:
    phone_book = [{"Дядя Петя": {"phone_numbers": [9998881234, 9997772233], "birth_day": "121276", "email": "mail@mail.ss"}, 
                   "Тетя Песя": {"phone_numbers": [9998881444]}}]
    save()

class AnotherWindow(QWidget):
    """
    This "window" is a QWidget. If it has no parent, it
    will appear as a free-floating window as we want.
    """
    def __init__(self):
        super().__init__()
        # self.build()
        # так получаем сыылку на родительское окно
        # self.parrent = self.parent()

        layout = QVBoxLayout()
        self.label = QLabel("Введите данные нового контакта")
        layout.addWidget(self.label)
        self.line0 = QLineEdit()
        self.line0.setPlaceholderText("Введите имя")
        layout.addWidget(self.line0)
        self.line1 = QLineEdit()
        self.line1.setPlaceholderText("Введите номер тел.1")
        layout.addWidget(self.line1)
        self.line2 = QLineEdit()
        self.line2.setPlaceholderText("Введите номер тел.2")
        layout.addWidget(self.line2)
        self.line3 = QLineEdit()
        self.line3.setPlaceholderText("Введите дату рождения")
        layout.addWidget(self.line3)
        self.line4 = QLineEdit()
        self.line4.setPlaceholderText("Введите email")
        layout.addWidget(self.line4)
        self.save_but = QtWidgets.QPushButton()
        self.save_but.setObjectName("sv_but")
        self.save_but.setText("Сохранить данные")
        layout.addWidget(self.save_but)
        self.setLayout(layout)
        self.save_but.clicked.connect(self.save_contact)
        
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
        phone_book[name_contact] = {"phone_numbers": [num_contact1, num_contact2], "birth_day": new_birth_day, "email": new_mail}
        save()

        # if Phone_bk().:
        #     Phone_bk().fill_table()
        # else:
        #     print("Error!!!!")
        
        self.hide()
        # phone_bk = Phone_bk()

        # self.parent.
        



class Phone_bk(QtWidgets.QMainWindow):

    tmp_phone_book = {}

    def __init__(self):
        super(Phone_bk, self).__init__()
        self.w = AnotherWindow()
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
        # self.ui.hlp_but.clicked.connect(self.hlp_contact)
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
                col+=1
                if str(type(temp_dict[key])) == "<class 'list'>":
                    temp_str = ', '.join(str(i) for i in temp_dict[key])
                    newitem = QStandardItem(temp_str)
                else:
                    newitem = QStandardItem(temp_dict[key])

                model.setItem(row, col, newitem)
            row+=1
    
        # Устанавливаем заголовки таблицы
        header_labels = ["Имя", "Телефоны", "Дата рождения", "E-mail"]
        for column in range(4):
            model.setHeaderData(column, Qt.Orientation.Horizontal, header_labels[column])
    
    # def add_cont(self):
        # name_contact, ok = QInputDialog.getText(
        #     self,
        #     "Имя нового контакта",
        #     "1 Введите имя",
        # )
        # num_contact1, ok = QInputDialog.getText(
        #     self,
        #     "Телефон1",
        #     "2 Введите 1й номер:",
        # )
        # num_contact2, ok = QInputDialog.getText(
        #     self,
        #     "Телефон2",
        #     "3 Введите 2й номер:",
        # )
        # new_birth_day, ok = QInputDialog.getText(
        #     self,
        #     "День рождения",
        #     "4 Введите день рождение:",
        # )
        # new_mail, ok = QInputDialog.getText(
        #     self,
        #     "Электронная почта",
        #     "5 Введите e-mail",
        # )
        # if ok:
        #     phone_book[name_contact] = {"phone_numbers": [num_contact1, num_contact2], "birth_day": new_birth_day, "email": new_mail}

        # save()
        # self.fill_table()

    def del_contact(self):
        name_delete, ok = QInputDialog.getText(
            self,
            "Удаление контакта",
            "Введите имя удаляемого контакта",
        )
        if ok:
            try:
                del phone_book [name_delete]
                dialog = QMessageBox(parent=self, text=f"Контакт ''{name_delete}'' удален из списка")
                dialog.setWindowTitle("Delete Dialog")
            except:
                dialog = QMessageBox(parent=self, text=f"Контакт ''{name_delete}'' отсутствует в списке, удаление возможно по полному имени")
                dialog.setWindowTitle("Delete Dialog")
            save()
            load()
            self.fill_table()

    def red_contact(self):
        name_find_red, ok = QInputDialog.getText(
            self,
            "Поиск контакта",
            "Введите имя искомого контакта",
        )
        if ok:
            if name_find_red in phone_book:
                text_c = f"Имя контакта {name_find_red}\n"
                temp_dict = phone_book[name_find_red]
                temp_key = "phone_numbers"
                text_c += f"Номер(а) телефона(ов) {temp_dict[temp_key]}\n"
                
                try:
                    temp_key = "birth_day"
                    text_c += f"День рождение: {temp_dict[temp_key]}\n"
                except:
                    pass
                try:
                    temp_key = "email"
                    text_c += f"E-mail: {temp_dict[temp_key]}"
                except:
                    pass

                dialog = QMessageBox(parent=self, text=text_c)
                dialog.setWindowTitle("Find Dialog")
                ret = dialog.exec()
            else:
                dialog = QMessageBox(parent=self, text=f"Контакт ''{name_find_red}'' отсутствует в списке")
                dialog.setWindowTitle("Find Dialog")
                ret = dialog.exec()

        name_contact, ok = QInputDialog.getText(
            self,
            "Имя нового контакта",
            "1 Введите имя", 
            QtWidgets.QLineEdit.EchoMode.Normal,
            name_find_red
        )
        num_contact1, ok = QInputDialog.getText(
            self,
            "Телефон1",
            "2 Введите 1й номер:",
            QtWidgets.QLineEdit.EchoMode.Normal,
            str(temp_dict["phone_numbers"][0])
        )
        try:
            temp_num2 = str(temp_dict["phone_numbers"][1])
        except:
            temp_num2 = ""

        num_contact2, ok = QInputDialog.getText(
            self,
            "Телефон2",
            "3 Введите 2й номер:",
            QtWidgets.QLineEdit.EchoMode.Normal,
            temp_num2
        )
        try:
            temp_bday = str(temp_dict["birth_day"][1])
        except:
            temp_bday = ""

        new_birth_day, ok = QInputDialog.getText(
            self,
            "День рождения",
            "4 Введите день рождение:",
            QtWidgets.QLineEdit.EchoMode.Normal,
            temp_bday
        )

        try:
            temp_mail = temp_dict["email"][1]
        except:
            temp_mail = ""

        new_mail, ok = QInputDialog.getText(
            self,
            "Электронная почта",
            "5 Введите e-mail",
            QtWidgets.QLineEdit.EchoMode.Normal,
            temp_mail
        )
        
        if ok:
            del phone_book[name_find_red]
            phone_book[name_contact] = {"phone_numbers": [num_contact1, num_contact2], "birth_day": new_birth_day, "email": new_mail}
            save()
            load()
            self.fill_table()
    
    def fnd_contact(self):

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
                        col+=1
                        if str(type(temp_dict[key])) == "<class 'list'>":
                            temp_str = ', '.join(str(i) for i in temp_dict[key])
                            newitem = QStandardItem(temp_str)
                        else:
                            newitem = QStandardItem(temp_dict[key])
                            newitem.emitDataChanged()

                        model.setItem(row, col, newitem)
                    row+=1
            
                # Устанавливаем заголовки таблицы
                header_labels = ["Имя", "Телефоны", "Дата рождения", "E-mail"]
                for column in range(4):
                    model.setHeaderData(column, Qt.Orientation.Horizontal, header_labels[column])
  

            if not_found:
                dialog = QMessageBox(parent=self, text=f"Контакт ''{name_find}'' отсутствует в списке")
                dialog.setWindowTitle("Find Dialog")
                ret = dialog.exec()
            
            self.tmp_phone_book = {}

    def add_cont(self):
        # try:
        #     if self.w is None:
        #         self.w = AnotherWindow()
        # except:
        #     self.w = AnotherWindow()
        #     pass
        # print("hlp_contact нажат")
        self.w.show()
        # self.fill_table()
        

    # def deleteSelected(self):
    #     # TODO
    #     pass

app = QtWidgets.QApplication([])
application = Phone_bk()
application.show()
save()
sys.exit(app.exec())
