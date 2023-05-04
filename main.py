from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton
from app import Dodger
from menu import Menu


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # Создание экземпляров классов первого и второго окна
        self.first_window = Menu()
        # Привязка сигнала нажатия кнопки на первом окне к слоту, который скрывает первое окно и отображает второе
        self.first_window.start_button.clicked.connect(self.play)

    def play(self):
        self.first_window.hide()
        self.game = Dodger()
        self.game.show()


if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.first_window.show()  # Отображение первого окна при запуске
    app.exec_()
