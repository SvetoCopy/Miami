from PyQt5.QtCore import Qt, QBasicTimer, QTimer
from PyQt5.QtGui import QPainter, QPixmap, QPen, QFont, QFontDatabase
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox, QLabel, QMainWindow
from random import randint, choice
from PyQt5 import QtWidgets, uic

WIN_X = 400
WIN_Y = 50
WIN_WIDTH = 400
WIN_HEIGHT = 900
DECOR_WIDTH = 400
WIN_WIDTH += 2*DECOR_WIDTH
CAR_WIDTH = 30
CAR_HEIGHT = 55
CAR_STEP_X = 40
CAR_STEP_Y = 10


class Obstacle:
    def __init__(self, texture):
        self.x = 0
        self.y = -35
        self.width = CAR_WIDTH
        self.height = CAR_HEIGHT
        self.image = texture
        self.passed_start = False

    def move(self):
        self.y += 5

    def draw(self, qp):
        qp.drawPixmap(self.x, self.y, self.width, self.height, self.image)

    def choose_road(self, roads):
        while True:
            road_num = randint(0, 9)
            road = roads[road_num]
            if road.is_free_start:
                road.fill_start(self)
                self.x = DECOR_WIDTH + ((WIN_WIDTH - 2*DECOR_WIDTH) // 10) * road_num
                break


class Road:
    def __init__(self):
        self.is_free_start = True
        self.start_car = 0
        self.moving_cars = []

    def move(self):
        for obstacle in self.moving_cars:
            obstacle.move()
            if obstacle.y >= WIN_HEIGHT:
                self.moving_cars.remove(obstacle)
        if self.is_free_start is False:
            if self.start_car.y >= self.start_car.height + 10:
                self.is_free_start = True

    def checkCollision(self, player):
        for obstacle in self.moving_cars:
            if (player.x + player.width > obstacle.x and
                    player.x < obstacle.x + obstacle.width and
                    player.y + player.height > obstacle.y and
                    player.y < obstacle.y + obstacle.height):
                return True
        return False

    def draw(self, qp):
        for obstacle in self.moving_cars:
            obstacle.draw(qp)

    def clear_start(self):
        self.is_free_start = True
        self.moving_cars.append(self.start_car)

    def fill_start(self, car):
        self.is_free_start = False
        self.start_car = car
        self.moving_cars.append(car)


class Player:
    def __init__(self, texture):
        self.x = WIN_WIDTH // 2
        self.y = WIN_HEIGHT - 100
        self.width = CAR_WIDTH
        self.height = CAR_HEIGHT
        self.image = QPixmap(texture)

    def move(self, e):
        if e.key() == Qt.Key_Left and self.x - CAR_STEP_X >= DECOR_WIDTH:
            self.x -= CAR_STEP_X
        elif e.key() == Qt.Key_Right and self.x + CAR_STEP_X < WIN_WIDTH-DECOR_WIDTH:
            self.x += CAR_STEP_X
        elif e.key() == Qt.Key_Up and self.y - CAR_STEP_Y >= DECOR_WIDTH:
            self.y -= CAR_STEP_Y
        elif e.key() == Qt.Key_Down and self.y + CAR_STEP_Y < WIN_HEIGHT:
            self.y += CAR_STEP_Y

    def draw(self, qp):
        qp.drawPixmap(self.x, self.y, self.width, self.height, self.image)


class FailWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        #self.setFixedSize(851,  551)
        uic.loadUi('retry.ui', self)
        self.quit_button.clicked.connect(self.quit)


    def quit(self):
        exit()

class Dodger(QWidget):

    def __init__(self):
        super().__init__()
        self.setGeometry(WIN_X, WIN_Y, WIN_WIDTH, WIN_HEIGHT)  # по 25 на каждую трассу
        self.setWindowTitle('HotTrack Miami')
        self.setFixedSize(WIN_WIDTH, WIN_HEIGHT)

        self.obst_textures = [QPixmap('obst_car1.png'), QPixmap('obst_car2.png'), QPixmap('obst_car1.png'),
                              QPixmap('obst_car4.png'), QPixmap('obst_car5.png'), QPixmap('obst_car6.png')]
        self.player_texture = QPixmap('gg_car.png')
        self.road_pixmap = QPixmap('doroga.png')
        self.bush_pixmap = QPixmap('kusti.png')
        self.obstacles = []
        self.road_offset = 0

        self.score_label = QLabel(self)
        self.score_label.setGeometry(30, 30, 330, 50)
        self.score_label.setAlignment(Qt.AlignCenter)
        self.score_pixmap = QPixmap('text_fon1.png')
        self.score_label.setPixmap(self.score_pixmap)
        fontId = QFontDatabase.addApplicationFont("justicechrome.ttf")
        fontName = QFontDatabase.applicationFontFamilies(fontId)[0]
        self.score_label.setFont(QFont(fontName, 20))

        self.difficulty_label = QLabel(self)
        self.difficulty_label.setGeometry(850, 30, 330, 50)
        self.difficulty_label.setAlignment(Qt.AlignCenter)
        self.difficulty_pixmap = QPixmap('text_fon2.png')
        self.difficulty_label.setPixmap(self.difficulty_pixmap)
        self.difficulty_label.setFont(QFont(fontName, 20))

        self.startGame()

    def startGame(self):
        self.player = Player(self.player_texture)
        self.roads = [Road() for x in range(10)]

        self.spawn_timer = QTimer(self)
        self.spawn_timer.timeout.connect(self.spawnTimer)
        self.spawn_timer.start(400)

        self.move_timer = QTimer(self)
        self.move_timer.timeout.connect(self.moveTimer)
        self.move_timer.start(20)

        self.score_timer = QTimer(self)
        self.score_timer.timeout.connect(self.scoreTimer)
        self.score_timer.start(50)

        self.road_timer = QTimer(self)
        self.road_timer.timeout.connect(self.roadTimer)
        self.road_timer.start(20)

        self.score = 0  # переменная для хранения очков
        self.difficulty = 'LOX'

        self.difficulty_label.setText(self.difficulty)
        self.score_label.setText('SCORE: '+str(self.score))

    def upgrade_difficulty(self):
        if self.move_timer.interval() < 6:
            return
        elif self.move_timer.interval() < 10:
            self.difficulty = "HAHAHAHAHAHAHAH"
        elif self.move_timer.interval() < 15:
            self.difficulty = 'PRO GAMER 2004'
        elif self.move_timer.interval() < 21:
            self.difficulty = 'NORMAL`NO TAK'

        self.difficulty_label.setText(self.difficulty)
        self.move_timer.start(self.move_timer.interval() - 1)
        self.spawn_timer.start(self.spawn_timer.interval() - 15)
        self.road_timer.start(self.road_timer.interval() - 1)

    def roadTimer(self):
        self.road_offset += 12
        if self.road_offset >= self.height():
            self.road_offset = 0
        self.repaint()
        self.update()

    def scoreTimer(self):
        self.score += 1  # увеличиваем количество очков
        self.score_label.setText(f'SCORE: {self.score}')

        if self.score % 100 == 0:
            self.upgrade_difficulty()

    def spawnTimer(self):
        car = Obstacle(choice(self.obst_textures))
        car.choose_road(self.roads)
        self.update()

    def moveTimer(self):
        for road in self.roads:
            road.move()
            if road.checkCollision(self.player):
                self.score_timer.stop()
                self.spawn_timer.stop()
                self.move_timer.stop()
                self.road_timer.stop()
                self.RetryBox = FailWindow()
                self.RetryBox.show()
                self.RetryBox.retry_button.clicked.connect(self.retry)
                break

        self.update()

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        # Я поставил тут -200 к ширине
        qp.drawPixmap(DECOR_WIDTH, self.road_offset, self.width() - 2*DECOR_WIDTH, self.height(), self.road_pixmap)
        qp.drawPixmap(DECOR_WIDTH, self.road_offset - self.height(), self.width() - 2*DECOR_WIDTH, self.height(), self.road_pixmap)

        qp.drawPixmap(0, self.road_offset, DECOR_WIDTH, self.height(), self.bush_pixmap)
        qp.drawPixmap(0, self.road_offset - self.height(), DECOR_WIDTH, self.height(), self.bush_pixmap)
        qp.drawPixmap(WIN_WIDTH-DECOR_WIDTH, self.road_offset, DECOR_WIDTH, self.height(), self.bush_pixmap)
        qp.drawPixmap(WIN_WIDTH-DECOR_WIDTH, self.road_offset - self.height(), DECOR_WIDTH, self.height(), self.bush_pixmap)

        qp.drawPixmap(30, 30, 330, 50, self.score_pixmap)
        qp.drawPixmap(850, 30, 330, 50, self.difficulty_pixmap)
        self.player.draw(qp)

        for road in self.roads:
            road.draw(qp)
        qp.end()

    def retry(self):
        self.startGame()
        self.RetryBox.hide()

    def keyPressEvent(self, e):
        self.player.move(e)
        self.update()


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    dodger = Dodger()
    dodger.show()
    sys.exit(app.exec_())