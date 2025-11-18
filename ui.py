from prf_math import GCDFunction, LCMFunction


class ConsoleUI:
    def __init__(self):
        self.gcd_func = GCDFunction()
        self.lcm_func = LCMFunction()

    def display_menu(self):
        print("\n" + "=" * 50)
        print("   Калькулятор НОД и НОК через ПРФ")
        print("=" * 50)
        print("1. Вычислить НОД двух чисел")
        print("2. Вычислить НОК двух чисел")
        print("3. Вычислить НОД и НОК")
        print("4. Показать примеры")
        print("5. Выход")
        print("-" * 50)

    def get_number(self, prompt):
        while True:
            try:
                return int(input(prompt))
            except ValueError:
                print("Ошибка: введите целое число!")

    def compute_gcd(self):
        print("\nВычисление НОД")
        a = self.get_number("Введите первое число: ")
        b = self.get_number("Введите второе число: ")
        result = self.gcd_func(a, b)
        print(f"НОД({a}, {b}) = {result}")

    def compute_lcm(self):
        print("\nВычисление НОК")
        a = self.get_number("Введите первое число: ")
        b = self.get_number("Введите второе число: ")
        result = self.lcm_func(a, b)
        print(f"НОК({a}, {b}) = {result}")

    def compute_both(self):
        print("\nВычисление НОД и НОК")
        a = self.get_number("Введите первое число: ")
        b = self.get_number("Введите второе число: ")
        gcd_result = self.gcd_func(a, b)
        lcm_result = self.lcm_func(a, b)
        print(f"НОД({a}, {b}) = {gcd_result}")
        print(f"НОК({a}, {b}) = {lcm_result}")
        print(f"Проверка: {a} × {b} = {a * b}, НОД × НОК = {gcd_result * lcm_result}")

    def show_examples(self):
        print("\nПримеры вычислений")
        examples = [
            (48, 18), (56, 42), (1071, 462),
            (17, 13), (100, 25), (8, 12)
        ]

        print("Числа\t\tНОД\tНОК\tПроверка")
        print("-" * 40)
        for a, b in examples:
            gcd_val = self.gcd_func(a, b)
            lcm_val = self.lcm_func(a, b)
            check = "✓" if a * b == gcd_val * lcm_val else "✗"
            print(f"{a}, {b}\t\t{gcd_val}\t{lcm_val}\t{check}")

    def run(self):
        print("Добро пожаловать в калькулятор НОД/НОК!")
        print("Используется реализация через примитивно рекурсивные функции")

        while True:
            self.display_menu()
            choice = input("Выберите действие (1-5): ").strip()

            if choice == '1':
                self.compute_gcd()
            elif choice == '2':
                self.compute_lcm()
            elif choice == '3':
                self.compute_both()
            elif choice == '4':
                self.show_examples()
            elif choice == '5':
                print("До свидания!")
                break
            else:
                print("Неверный выбор! Попробуйте снова.")

            input("\nНажмите Enter для продолжения...")