import sys
import requests
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
from PyQt5.QtWidgets import QLabel, QLineEdit
from PyQt5.QtGui import QPixmap


class Input(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 350, 300)
        self.setWindowTitle('Ввод данных')

        self.btn = QPushButton('Принять', self)
        self.btn.resize(self.btn.sizeHint())
        self.btn.move(100, 150)
        self.btn.clicked.connect(self.accept)

        self.coord1 = QLineEdit(self)
        self.coord1.move(200, 30)

        self.text1 = QLabel(self)
        self.text1.setText('Введите долготу:')
        self.text1.move(50, 30)

        self.coord2 = QLineEdit(self)
        self.coord2.move(200, 70)

        self.text2 = QLabel(self)
        self.text2.setText('Введите широту:')
        self.text2.move(50, 70)

        self.scale = QLineEdit(self)
        self.scale.move(200, 110)

        self.text3 = QLabel(self)
        self.text3.setText('Введите масштаб:')
        self.text3.move(50, 110)

    def accept(self):
        lon = self.coord1.text()
        lat = self.coord2.text()
        delta = self.scale.text()
        self.map = Map(lon, lat, delta)
        self.map.show()


class Map(QWidget):
    def __init__(self, lon, lat, delt):
        self.lon = lon
        self.lat = lat
        self.delta = delt
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(100, 200, 600, 450)
        self.setWindowTitle('Карта')
        api_server = "http://static-maps.yandex.ru/1.x/"
        params = {
            "ll": ",".join([self.lon, self.lat]),
            "spn": ",".join([self.delta, self.delta]),
            "l": "map"
        }
        response = requests.get(api_server, params=params)
        if not response:
            sys.exit()
        map_file = "map.png"
        with open(map_file, "wb") as file:
            file.write(response.content)
        self.pixmap = QPixmap('map.png')
        self.image = QLabel(self)
        self.image.move(0, 0)
        self.image.resize(600, 450)
        self.image.setPixmap(self.pixmap)


def except_hook(cls, exception, traceback):  # функция для вывода ошибок в консоль
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Input()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())