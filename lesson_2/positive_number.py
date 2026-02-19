def get_positive_number(prompt):
    """Безопасно получает положительное число от пользователя"""
    while True:
        try:
            number = float(input(prompt))
            if number <= 0:
                print("Число должно быть положительным!")
                continue
            return number
        except ValueError:
            print("Пожалуйста, введите корректное число!")
        except KeyboardInterrupt:
            print("\nПрограмма прервана пользователем")
            return None

# Использование
age = get_positive_number("Введите ваш возраст: ")
if age is not None:
    print(f"Ваш возраст: {age:.0f}")