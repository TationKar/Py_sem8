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


# ВЕРСИЯ ДЛЯ КОНСОЛИ

import json

def load():
    with open("contact.json", "r", encoding="utf-8") as fh:
        global phone_book
        phone_book = json.load(fh)
    print("Загрузка контактов выполнена успешно")
    # return phone_book

def save():
    with open("contact.json", "w", encoding="utf-8") as fh:
        fh.write(json.dumps(phone_book, ensure_ascii=False))
    print("Справочник сохранен")

try:
    load()
except:
    phone_book = {"Дядя Петя": {"phone_numbers": [9998881234, 9997772233], "birth_day": "121276", "email": "mail@mail.ss"}, 
    "Тетя Песя": {"phone_numbers": [9998881444]}}

while True:
    command = input("Введите команду: ")
    if command == "/add":
        name = input("Введите имя нового контакта: ")
        number0 = input("Введите 1й номер: ")
        number1 = input("Введите 2й номер: ")
        bith_day = input("Введите ДР: ")
        mail = input("Введите email: ")
        phone_book[name] = {"phone_numbers": [number0, number1], "birth_day": bith_day, "email": mail}
        print("Контакт добавлен")
    elif command == "/all":
        print("Список всех контактов")
        print(phone_book)
    elif command == "/find":
        name = input("Введите имя для поиска: ")
        not_found = True
        for contact in phone_book:
            if name in contact:
                not_found = False
                print(f"''{name}'' - найдено в контакте: {contact} {phone_book[contact]}")
        if not_found:
            print(f"Контакт ''{name}'' не найден в справочнике")
    elif command == "/save":
        save()
    elif command == "/load":
        phone_book = load()
        print("Загрузка контактов выполнена успешно")
    elif command == "/exit":
        save()
        print("Справочник закончил свою работу")
        break
    elif command == "/help":
        print("Список команд:")
        print("/exit    Выйти из справочника")
        print("/all     Вывести весь список")
        print("/add     Добавить новый контакт")
        print("/delete  Удалить контакт")
        print("/save    Сохранить список")
        print("/load    Загрузить список")
        print("/help    Вывод данного списка комманд")
    elif command == "/delete":
        name = input("Введите имя для поиска: ")
        try:
            del phone_book [name]
            print(f"Контакт ''{name}'' удален из списка")
        except:
            print(f"Контакт ''{name}'' отсутствует в списке, для удаления нужно ввести полное имя")
        save()
    else:
        print("Такой команды нет. Изучите, пожалуйста, руководство пользователя. Команда /help")