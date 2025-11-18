from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                               QGroupBox, QLabel, QLineEdit, QPushButton,
                               QComboBox, QTextEdit, QSplitter, QFileDialog)
from PySide6.QtCore import Qt
from PySide6.QtGui import QAction, QIntValidator
from prf_math import GCDFunction, LCMFunction
from datetime import datetime
from database.dbmanager import DatabaseManager


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.gcd_func = GCDFunction()
        self.lcm_func = LCMFunction()
        self.recursion_steps = []
        self.db_manager = DatabaseManager()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Калькулятор НОД и НОК - Примитивная рекурсия")
        self.setGeometry(100, 100, 1200, 800)

        # Создаем меню
        self.create_menu()

        # Главный виджет
        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        # Основной layout
        main_layout = QHBoxLayout(main_widget)

        # Разделитель
        splitter = QSplitter(Qt.Horizontal)

        # Левая часть - ввод и результаты
        left_widget = self.create_left_panel()

        # Правая часть - визуализация
        right_widget = self.create_right_panel()

        splitter.addWidget(left_widget)
        splitter.addWidget(right_widget)
        splitter.setSizes([600, 600])

        main_layout.addWidget(splitter)

    def create_menu(self):
        menubar = self.menuBar()

        # Меню Файл
        file_menu = menubar.addMenu("Файл")

        clear_action = QAction("Очистить", self)
        clear_action.triggered.connect(self.clear_all)
        file_menu.addAction(clear_action)

        export_action = QAction("Экспорт результата", self)
        export_action.triggered.connect(self.export_results)
        file_menu.addAction(export_action)

        save_to_db_action = QAction("Сохранить в базу данных", self)
        save_to_db_action.triggered.connect(self.save_to_database)
        file_menu.addAction(save_to_db_action)

        file_menu.addSeparator()

        view_db_action = QAction("Просмотр базы данных", self)
        view_db_action.triggered.connect(self.view_database)
        file_menu.addAction(view_db_action)

        file_menu.addSeparator()

        clear_db_action = QAction("Очистить базу данных", self)
        clear_db_action.triggered.connect(self.clear_database)
        file_menu.addAction(clear_db_action)

        exit_action = QAction("Выход", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # Меню Справка
        help_menu = menubar.addMenu("Справка")
        about_action = QAction("О программе", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

    def create_left_panel(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)

        # Группа ввода данных
        input_group = QGroupBox("Ввод данных")
        input_layout = QVBoxLayout(input_group)

        numbers_layout = QHBoxLayout()
        numbers_layout.addWidget(QLabel("Число A:"))
        self.number_a_edit = QLineEdit()
        self.number_a_edit.setPlaceholderText("Введите натуральное число (0-10000)")
        self.number_a_edit.setValidator(QIntValidator(0, 10000, self))
        numbers_layout.addWidget(self.number_a_edit)

        numbers_layout.addWidget(QLabel("Число B:"))
        self.number_b_edit = QLineEdit()
        self.number_b_edit.setPlaceholderText("Введите натуральное число (0-10000)")
        self.number_b_edit.setValidator(QIntValidator(0, 10000, self))
        numbers_layout.addWidget(self.number_b_edit)

        input_layout.addLayout(numbers_layout)

        # Выбор операции
        operation_layout = QHBoxLayout()
        operation_layout.addWidget(QLabel("Операция:"))
        self.operation_combo = QComboBox()
        self.operation_combo.addItems(["НОД", "НОК", "НОД и НОК"])
        operation_layout.addWidget(self.operation_combo)

        # Кнопка вычисления
        self.calculate_btn = QPushButton("Вычислить")
        self.calculate_btn.clicked.connect(self.calculate)
        operation_layout.addWidget(self.calculate_btn)

        input_layout.addLayout(operation_layout)
        layout.addWidget(input_group)

        # Группа результатов
        self.result_group = QGroupBox("Результаты")
        result_layout = QVBoxLayout(self.result_group)

        self.result_text = QTextEdit()
        self.result_text.setReadOnly(True)
        result_layout.addWidget(self.result_text)

        layout.addWidget(self.result_group)

        # Группа статистики
        self.stats_group = QGroupBox("Статистика вычислений")
        stats_layout = QVBoxLayout(self.stats_group)

        self.stats_text = QTextEdit()
        self.stats_text.setReadOnly(True)
        self.stats_text.setMaximumHeight(150)
        stats_layout.addWidget(self.stats_text)

        layout.addWidget(self.stats_group)

        return widget

    def create_right_panel(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)

        # Группа визуализации
        viz_group = QGroupBox("Визуализация примитивной рекурсии")
        viz_layout = QVBoxLayout(viz_group)

        self.visualization_text = QTextEdit()
        self.visualization_text.setReadOnly(True)
        viz_layout.addWidget(self.visualization_text)

        # Информация о ПРФ
        info_label = QLabel(
            "Примитивно рекурсивные функции:\n"
            "• Базовые: Z(), S(), P_i^n()\n"
            "• Композиция: f(g1,...,gn)\n"
            "• Примитивная рекурсия: f(0)=g(), f(n+1)=h(n,f(n))"
        )
        info_label.setStyleSheet("background-color: #f0f0f0; padding: 10px; border-radius: 5px;")
        viz_layout.addWidget(info_label)

        layout.addWidget(viz_group)

        return widget

    def calculate(self):
        # Получаем введенные значения
        a_text = self.number_a_edit.text().strip()
        b_text = self.number_b_edit.text().strip()

        # Проверка на пустые поля
        if not a_text or not b_text:
            self.result_text.setText("Ошибка: введите оба числа!")
            return

        # Проверка, что введены числа. Вообще, это уже невозможно ввиду блока ввода данных
        try:
            a = int(a_text)
            b = int(b_text)
        except ValueError:
            self.result_text.setText("Ошибка: введите корректные целые числа!")
            return

        # Проверка, что числа натуральные (≥ 0)
        if a < 0 or b < 0:
            self.result_text.setText("Ошибка: числа должны быть натуральными (≥ 0)!")
            return

        # Проверка, на слишком большие числа
        if a > 10000 or b > 10000:
            self.result_text.setText("Ошибка: числа не должны превышать 10000!")
            return

        # Если все проверки пройдены, выполняем вычисления
        try:
            operation = self.operation_combo.currentText()

            self.recursion_steps = []
            result_text = ""
            stats_text = ""

            if operation == "НОД":
                result = self.gcd_func(a, b)
                result_text = f"НОД({a}, {b}) = {result}"

            elif operation == "НОК":
                gcd_val = self.gcd_func(a, b)
                result = self.lcm_func(a, b)
                result_text = f"НОК({a}, {b}) = {result}"

            else:  # НОД и НОК
                gcd_result = self.gcd_func(a, b)
                lcm_result = self.lcm_func(a, b)
                result_text = (f"НОД({a}, {b}) = {gcd_result}\n"
                               f"НОК({a}, {b}) = {lcm_result}\n\n")

            # Статистика
            stats_text = self.generate_stats(a, b, operation)

            # Визуализация
            viz_text = self.generate_visualization(a, b, operation)

            self.result_text.setText(result_text)
            self.stats_text.setText(stats_text)
            self.visualization_text.setText(viz_text)

        except RecursionError:
            self.result_text.setText("Ошибка: слишком глубокая рекурсия! Попробуйте меньшие числа.")
        except Exception as e:
            self.result_text.setText(f"Ошибка вычисления: {str(e)}")

    def generate_stats(self, a, b, operation):
        stats = []
        stats.append("СТАТИСТИКА ВЫЧИСЛЕНИЙ")
        stats.append(f"Число A: {a}")
        stats.append(f"Число B: {b}")
        stats.append(f"Операция: {operation}")
        gcd_val = self.gcd_func(a, b)
        if operation in ["НОД", "НОД и НОК"]:
            stats.append(f"НОД: {gcd_val}")
            stats.append(f"Делители {a}: {self.get_divisors(a)}")
            stats.append(f"Делители {b}: {self.get_divisors(b)}")
            stats.append(f"Общие делители: {self.get_common_divisors(a, b)}")

        if operation in ["НОК", "НОД и НОК"]:
            lcm_val = self.lcm_func(a, b)
            stats.append(f"НОК: {lcm_val}")
            stats.append(f"Проверка: {a} × {b} = НОД × НОК = {gcd_val * lcm_val}")

        return "\n".join(stats)

    def generate_visualization(self, a, b, operation):
        viz = []
        viz.append("ПРОЦЕСС ВЫЧИСЛЕНИЯ")

        if operation == "НОД":
            viz.append(f"Вычисление НОД({a}, {b}):")
            viz.extend(self.visualize_gcd(a, b, 0))
        elif operation == "НОК":
            viz.append(f"Вычисление НОК({a}, {b}):")
            viz.extend(self.visualize_lcm(a, b))
        else:
            viz.append(f"Вычисление НОД({a}, {b}) и НОК({a}, {b}):")
            viz.extend(self.visualize_gcd(a, b, 0))
            viz.append("\n Вычисление НОК")
            viz.extend(self.visualize_lcm(a, b))

        return "\n".join(viz)

    def visualize_gcd(self, a, b, depth):
        steps = []
        indent = "  " * depth

        if b == 0:
            steps.append(f"{indent}НОД({a}, {b}) = {a} (базовый случай)")
            return steps

        steps.append(f"{indent}НОД({a}, {b})")

        if a >= b:
            new_a = b
            new_b = a - b
            steps.append(f"{indent}→ НОД({new_a}, {new_b}) (рекурсивный шаг)")
            steps.extend(self.visualize_gcd(new_a, new_b, depth + 1))
        else:
            new_a = a
            new_b = b - a
            steps.append(f"{indent}→ НОД({new_a}, {new_b}) (рекурсивный шаг)")
            steps.extend(self.visualize_gcd(new_a, new_b, depth + 1))

        return steps

    def visualize_lcm(self, a, b):
        steps = []
        steps.append(f"НОК({a}, {b}) = ({a} × {b}) / НОД({a}, {b})")
        gcd_val = self.gcd_func(a, b)
        steps.append(f"НОК({a}, {b}) = {a * b} / {gcd_val}")
        steps.append(f"НОК({a}, {b}) = {(a * b) // gcd_val}")
        return steps

    def get_divisors(self, n):
        divisors = []
        for i in range(1, n + 1):
            if n % i == 0:
                divisors.append(i)
        return divisors[:10]  # Ограничиваем вывод

    def get_common_divisors(self, a, b):
        common = []
        for i in range(1, min(a, b) + 1):
            if a % i == 0 and b % i == 0:
                common.append(i)
        return common[:10]  # Ограничиваем вывод

    def clear_all(self):
        self.number_a_edit.clear()
        self.number_b_edit.clear()
        self.result_text.clear()
        self.stats_text.clear()
        self.visualization_text.clear()

    def show_about(self):
        about_text = (
            "Калькулятор НОД и НОК\n\n"
            "Реализован с использованием примитивно рекурсивных функций.\n"
            "Примитивная рекурсия гарантирует завершение вычислений\n"
            "для любых входных данных.\n\n"
        )
        self.result_text.setText(about_text)

    def export_results(self):
        """Экспорт текущих результатов в txt-файл"""

        # Проверяем, есть ли что экспортировать
        if not self.result_text.toPlainText().strip():
            self.result_text.setText("Ошибка: нет результатов для экспорта!")
            return

        # Диалог выбора файла
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Экспорт результатов",
            f"НОД_НОК_результат_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            "Text Files (*.txt)"
        )

        if not file_path:
            return  # Пользователь отменил

        try:
            with open(file_path, 'w', encoding='utf-8') as file:
                # Заголовок
                file.write("=" * 50 + "\n")
                file.write("РЕЗУЛЬТАТЫ ВЫЧИСЛЕНИЙ НОД и НОК\n")
                file.write("=" * 50 + "\n\n")

                # Дата и время
                file.write(f"Дата экспорта: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}\n\n")

                # Входные данные
                a_text = self.number_a_edit.text()
                b_text = self.number_b_edit.text()
                operation = self.operation_combo.currentText()

                if a_text and b_text:
                    file.write(f"ВХОДНЫЕ ДАННЫЕ:\n")
                    file.write(f"Число A: {a_text}\n")
                    file.write(f"Число B: {b_text}\n")
                    file.write(f"Операция: {operation}\n\n")

                # Основные результаты
                file.write("РЕЗУЛЬТАТЫ:\n")
                file.write("-" * 30 + "\n")
                file.write(self.result_text.toPlainText() + "\n\n")

                # Статистика
                stats_text = self.stats_text.toPlainText()
                if stats_text:
                    file.write("СТАТИСТИКА:\n")
                    file.write("-" * 30 + "\n")
                    file.write(stats_text + "\n\n")

                # Визуализация процесса
                viz_text = self.visualization_text.toPlainText()
                if viz_text:
                    file.write("ПРОЦЕСС ВЫЧИСЛЕНИЯ:\n")
                    file.write("-" * 30 + "\n")
                    file.write(viz_text + "\n\n")

                # Информация о программе
                file.write("ИНФОРМАЦИЯ О ПРОГРАММЕ:\n")
                file.write("-" * 30 + "\n")
                file.write("Калькулятор НОД и НОК\n")
                file.write("Реализован с использованием примитивно рекурсивных функций\n")
                file.write("Гарантированное завершение вычислений для любых входных данных\n")

            # Сообщение об успехе
            self.result_text.setText(
                f"Результаты успешно экспортированы в файл:\n{file_path}\n\n" +
                self.result_text.toPlainText()
            )

        except Exception as e:
            self.result_text.setText(f"Ошибка при экспорте: {str(e)}")

    def save_to_database(self):
        """Сохранение текущего результата в базу данных"""

        # Проверяем, есть ли результаты для сохранения
        if not self.result_text.toPlainText().strip():
            self.result_text.setText("Ошибка: нет результатов для сохранения!")
            return

        # Получаем текущие данные
        a_text = self.number_a_edit.text().strip()
        b_text = self.number_b_edit.text().strip()
        operation = self.operation_combo.currentText()

        if not a_text or not b_text:
            self.result_text.setText("Ошибка: нет входных данных для сохранения!")
            return

        try:
            a = int(a_text)
            b = int(b_text)

            # Определяем тип операции для БД
            if operation == "НОД":
                result = self.gcd_func(a, b)
                operation_type = "НОД"
            elif operation == "НОК":
                result = self.lcm_func(a, b)
                operation_type = "НОК"
            else:  # НОД и НОК
                # Для комбинированной операции сохраняем оба результата
                gcd_result = self.gcd_func(a, b)
                lcm_result = self.lcm_func(a, b)

                # Сохраняем НОД
                self.db_manager.save_calculation("НОД", a, b, gcd_result)
                # Сохраняем НОК
                self.db_manager.save_calculation("НОК", a, b, lcm_result)

                self.result_text.setText(
                    f"Результаты сохранены в базу данных!\n\n" +
                    self.result_text.toPlainText()
                )
                return

            # Сохраняем одиночную операцию
            record_id = self.db_manager.save_calculation(operation_type, a, b, result)

            self.result_text.setText(
                f"Результат сохранен в базу данных (ID: {record_id})!\n\n" +
                self.result_text.toPlainText()
            )

        except Exception as e:
            self.result_text.setText(f"Ошибка при сохранении в БД: {str(e)}")

    def view_database(self):
        """Простой просмотр базы данных"""
        from PySide6.QtWidgets import QMessageBox

        try:
            calculations = self.db_manager.get_all_calculations()
            stats = self.db_manager.get_statistics()

            db_text = "БАЗА ДАННЫХ РАСЧЕТОВ\n\n"

            # Статистика
            db_text += f"Всего записей: {stats['total_count']}\n"
            db_text += "Статистика по операциям:\n"
            for op_type, count in stats['type_stats']:
                db_text += f"  {op_type}: {count} записей\n"

            db_text += "\nПоследние записи:\n"
            db_text += "-" * 50 + "\n"

            if calculations:
                for calc in calculations[:10]:  # Показываем последние 10 записей
                    id_val, op_type, a, b, result, timestamp = calc

                    time_display = self.db_manager.format_timestamp(timestamp)
                    db_text += f"ID: {id_val} | {op_type}({a}, {b}) = {result} | {time_display}\n"
            else:
                db_text += "База данных пуста\n"

            # Показываем во всплывающем окне
            msg_box = QMessageBox(self)
            msg_box.setWindowTitle("База данных расчетов")
            msg_box.setText(db_text)


            # Увеличиваем размер окна
            msg_box.resize(600, 400)

            msg_box.exec()

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка при чтении базы данных: {str(e)}")

    def clear_database(self):
        from PySide6.QtWidgets import QMessageBox
        try:
            self.db_manager.clear_all_calculations()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка при очистке БД: {str(e)}")


