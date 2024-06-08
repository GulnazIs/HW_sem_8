# DictReader, DictWriter коснтуркторы, нужны только когда работаем со списком словарей, с txt не нужны
# DictReader получаем содержимое файла в виде набора словарей, где каждая строка отдельный словарь
# DictWriter мы имеем список словарей и отгружаем их сразу в файл

from csv import DictReader, DictWriter
from os.path import exists

class NameError(Exception):
    def init(self, txt):
        self.txt = txt

def get_info():
    flag = False
    while not flag:
        try:
            first_name = input ('Введите имя: ')
            if len(first_name) < 2:
                raise NameError('Слишком короткое имя')
            second_name = input('Введите фамилию: ')
            if len(second_name) < 5:
                raise NameError('Слишком короткая фамилия')
            phone_number = input('Введите номер телефона: ')
            if len(phone_number) < 11:
                raise NameError('Слишком короткий номер телефона')
        except NameError as err:
            print(err)
        else:
            flag = True
    return [first_name, second_name, phone_number]


def create_file(file_name):
    # with open - контекстный менеджер(менеджер контекста), utf-8 чтобы при чтении в другйо кодировке не было ошибки
    # data у нас файловый дескриптор,т.е. поток данных
    #'w'- если файла нет, то он создастся и будет производиться полная перезапись файла
    with open(file_name, 'w', encoding='utf-8', newline='') as data:
        f_w = DictWriter(data, fieldnames=['Имя', 'Фамилия', 'Телефон'])
        f_w.writeheader()


def write_file(file_name):
    user_data = get_info()
    res = read_file(file_name) 
    new_obj = {'first_name': user_data[0], 'second_name': user_data[1], 'phone_number': user_data[2]}
    res.append(new_obj)
    standart_write(file_name, res)


def read_file(file_name):
    with open(file_name, encoding='utf-8') as data:#по дефолту будет режим read
        f_r = DictReader(data)
        return list(f_r) #функция вернет список из словарей


def standart_write(file_name, res):
    with open(file_name, 'w', encoding='utf-8', newline='') as data:
        f_w = DictWriter(data, fieldnames=['first_name', 'second_name', 'phone_number'])
        f_w.writeheader()
        f_w.writerows(res)


def remove_row(file_name):
    search = int(input('Введите номер строки для удаления: '))
    res = read_file(file_name)
    if search <= len(res):
        res.pop(search - 1)
        standart_write(file_name, res)
    else:
        print('Введен несуществующий номер строки')


def copy_data(file_name):
    name_of_copy = input('Введите название файла: ') + '.csv'
    copy = read_file(file_name)
    standart_write(name_of_copy, copy)


def copy_row(file_name):
    name_of_copy = input('Введите название файла: ') + '.csv'
    if not exists(name_of_copy):
        command = input('Файл отсутствует, хотите создать файл? \n').lower()
        if command == 'да':
            create_file(name_of_copy)
    res = read_file(file_name)
    copy_of_res = read_file(name_of_copy)
    while True:
        row_numb = int(input('Введите номер строки для копирования или 0 для выхода из режима копирования строки \n'))
        if row_numb < 1:
            break
        elif row_numb >= 1:
            copied_row = res[row_numb - 1]
            copy_of_res.append(copied_row)
            standart_write(name_of_copy, copy_of_res)
        elif row_numb > len(res) or row_numb < 0:
            print('В файле нет строки с таким номером') 
            

file_name = 'phone.csv'
def main():
    while True: # или while 1, делаем бесконечный цикл
        command = input('Введите команду: \n Выйти: q \n Внести запись: w \n Вывести справочник: r \n Удалить строку: d \n Скопировать справочник в новый файл: c \n Скопировать определенную строку: cr \n')
        if command == 'q':
            break
        elif command == 'w':
            if not exists(file_name):
                create_file(file_name)
            write_file(file_name)
        elif command == 'r':
            if not exists(file_name):
                print('Файл отсутствует, пожалуйста , создайте файл')
                continue
            print(*read_file(file_name))
        elif command == 'd':
            if not exists(file_name):
                print('Файл отсутствует, пожалуйста , создайте файл')
                continue
            remove_row(file_name)
        elif command == 'c':
            if not exists(file_name):
                print('Файл отсутствует, пожалуйста , создайте файл')
                continue
            copy_data(file_name)
        elif command == 'cr':
            if not exists(file_name):
                print('Файл отсутствует, пожалуйста , создайте файл')
                continue
            copy_row(file_name)
       
       
main()
