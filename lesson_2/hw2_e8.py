
# Задача 8: Универсальный обработчик файлов
# Условие: Создайте функцию file_processor() для работы с файлами 
# (чтение, запись, добавление, информация о файле), которая обрабатывает 
# различные типы исключений.

class ModeException(Exception):
    pass

class NotAdditionInfoException(Exception):
    pass

def file_processor(file_path: str, mode: str='r', addition_info: str=''):

    try:
        if mode not in ['r', 'w', 'a']:
            raise ModeException

        if mode in ['w', 'a'] and not addition_info:
            raise NotAdditionInfoException

        file = open(file=file_path, mode=mode)

        if mode in ['w', 'a']:
            file.write(addition_info)
        else:
            print(file.read())

    except FileNotFoundError:
        print('File Not found')
    except ValueError:
        print('НЕверный тип значения')
    except ModeException:
        print('НЕверный режим открытия файла')
    except NotAdditionInfoException:
        print('Отсутствует информация для записи')


