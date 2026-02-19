"""
Калькулятор возраста
Условие: Напишите программу, которая запрашивает дату рождения пользователя и вычисляет
его возраст.
"""
import datetime

def yob_validation(p_yob):
    
    now = datetime.datetime.now()
    
    dob = datetime.datetime.strptime(p_yob, '%d.%m.%Y')
    print(f"Преобразовали введенное значение в {type(dob)}")
    message = "не смогли проверить"
    
    if dob > now:
        message = f"Вы не можете быть из будущего!"
    elif dob.date().year <= 1900:
        message = f"Вы попали в книгу рекордов Гиннесса!"
    else:
        years = (now - dob).days // 365
        message = f"Вам {years} лет"
        
    return message

yob = input("Введите свой год рождения в формате ДД.ММ.ГГГГ: ")

try:
    
    print(yob_validation(yob))
    
#except TypeError:
#    print(f"Вы ввели не число!")
except ValueError:
    print(f"Вы ввели не число!")