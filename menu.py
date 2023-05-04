from PyQt5 import QtCore

from PyQt5 import QtWidgets, uic

class Menu(QtWidgets.QMainWindow):
    switch_window_signal = QtCore.pyqtSignal(int)

    def __init__(self):
        super().__init__()

        self.setFixedSize(1000, 600)
        # Загружаем .ui файл
        uic.loadUi('menu.ui', self)
        # Устанавливаем обработчики для кнопок
        self.quit_button.clicked.connect(self.quit)


    def quit(self):
        exit()


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    menu = Menu()
    menu.show()
    app.exec_()
