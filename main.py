from ui import ConsoleUI
import sys
from PySide6.QtWidgets import QApplication
from gui import MainWindow

sys.setrecursionlimit(10000000)

def main():
    """Главная функция приложения"""
    app = QApplication(sys.argv)
    app.setStyle('windows11')
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()