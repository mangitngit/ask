import sys
import time
import random
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtTest import *
from PyQt5.QtWidgets import *
from PyQt5.QtMultimedia import QSound

wyyniki = []


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        self.central_widget = QStackedWidget()
        self.setCentralWidget(self.central_widget)

        self.start_screen = StartScreen()
        self.demo_screen = DemoScreen()
        self.test_screen = TestScreen()
        self.result_screen = ResultScreen()

        self.central_widget.addWidget(self.start_screen)
        self.central_widget.addWidget(self.demo_screen)
        self.central_widget.addWidget(self.test_screen)
        self.central_widget.addWidget(self.result_screen)
        self.resize(440, 400)

        self.central_widget.setCurrentWidget(self.start_screen)

        self.start_screen.demoClicked.connect(lambda: self.central_widget.setCurrentWidget(self.demo_screen))
        self.start_screen.testClicked.connect(lambda: self.central_widget.setCurrentWidget(self.test_screen))
        self.demo_screen.backClicked.connect(lambda: self.central_widget.setCurrentWidget(self.start_screen))
        self.test_screen.backClicked.connect(lambda: self.central_widget.setCurrentWidget(self.start_screen))
        self.test_screen.resultClicked.connect(lambda: self.central_widget.setCurrentWidget(self.result_screen))
        self.result_screen.backClicked.connect(lambda: self.central_widget.setCurrentWidget(self.start_screen))


def ad():
    wyyniki.append(350.12)
    wyyniki.append(334.21)
    wyyniki.append(420.12)
    wyyniki.append(592.23)
    wyyniki.append(505.23)
    wyyniki.append(523.11)


class StartScreen(QWidget):
    demoClicked = pyqtSignal()
    testClicked = pyqtSignal()

    def __init__(self):
        super(StartScreen, self).__init__()

        self.label = QLabel("Aby zacząc test kliknij przycisk Test.\n"
                            "Przed rozpoczęciem testu zaleca się\n"
                            " wykonanie treningu przez użycie przycisku Demo.", self)
        self.font = QFont('times', 13)
        self.demo = QPushButton('Demo', self)
        self.demo.setGeometry(QRect(30, 260, 180, 60))
        self.demo.clicked.connect(self.demo_clicked)

        self.test = QPushButton('Test', self)
        self.test.setGeometry(QRect(240, 260, 170, 60))
        self.test.clicked.connect(self.test_clicked)
        # self.test.setEnabled(False)

        self.prepare_labels()

    def prepare_labels(self):
        self.label.setFont(self.font)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setGeometry(QRect(20, 50, 400, 170))

    def demo_clicked(self):
        self.demoClicked.emit()
        self.test.setEnabled(True)

    def test_clicked(self):
        self.testClicked.emit()


class DemoScreen(QWidget):
    backClicked = pyqtSignal()

    def __init__(self):
        super(DemoScreen, self).__init__()
        self.time_start = 0
        self.time_stop = 0
        self.czas = 0
        self.square = QFrame(self)
        self.col = QColor(255, 0, 0)
        self.font = QFont('times', 13)
        self.czy_tekst = True

        self.label = QLabel(self)
        self.info = QLabel(self)
        self.wynik = QLabel(self)
        self.kroki = QLabel(self)

        self.back = QPushButton('Back', self)
        self.back.setGeometry(QRect(30, 30, 60, 20))
        self.back.clicked.connect(self.back_clicked)

        self.krok = 0
        self.kolor = 1
        self.rysuj()
        self.prepare_labels()

    def back_clicked(self):
        self.backClicked.emit()
        self.label.setText("Aby zacząć Demo - wciśnij Enter")

    def prepare_labels(self):

        self.label.setText("Aby zacząć Demo - wciśnij Enter")
        self.label.setFont(self.font)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setGeometry(QRect(20, -20, 400, 170))

        self.wynik.setFont(self.font)
        self.wynik.setGeometry(QRect(10, 300, 400, 170))

        self.info.setFont(self.font)
        self.info.setGeometry(QRect(120, 200, 400, 170))
        self.info.setHidden(True)

        self.kroki.setFont(self.font)
        self.kroki.setGeometry(QRect(350, 300, 400, 170))
        self.kroki.setText("próba {}/3".format(str(self.krok)))

    def rysuj(self):
        self.square.setGeometry(90, 100, 250, 250)
        self.square.setStyleSheet("QWidget { background-color: %s }" % self.col.name())

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter-1:
            if self.kolor == 1 and self.krok < 3:
                if self.czy_tekst:
                    self.label.setText("Gdy kolor będzie zielony\nnaciśnij Enter")
                    self.czy_tekst = False
                    self.label.setHidden(False)
                else:
                    self.label.setHidden(True)
                self.kolor = 2
                QTest.qWait(random.randint(1000, 3000))
                self.col.setRgb(0, 255, 0)
                self.square.setStyleSheet("QFrame { background-color: %s }" % self.col.name())
                self.time_start = time.time()

            elif self.kolor == 2 and self.krok < 3:
                self.time_stop = time.time()
                self.czas = (self.time_stop-self.time_start)*1000
                self.krok += 1
                self.kroki.setText("próba {}/3".format(str(self.krok)))
                self.wynik.setText("Wynik = {}".format(str(self.czas)[:5]))

                QTest.qWait(200)
                self.col.setRgb(255, 0, 0)
                self.square.setStyleSheet("QFrame { background-color: %s }" % self.col.name())
                self.label.setText("Naciśnij ENTER")
                self.label.setHidden(False)
                self.kolor = 1

            if self.krok == 3:
                self.square.repaint()
                self.square.setHidden(True)
                self.krok += 1
                self.czy_tekst = True
                self.kolor = 3
                self.kroki.setText("próba {}/3".format(0))
                self.label.setText("Test dźwiękowy - Naciśnij Enter")

            elif self.kolor == 3 and self.krok < 7:
                if self.czy_tekst:
                    self.czy_tekst = False
                    self.label.setText("Gdy usłyszysz dźwięk\nnaciśnij Enter")
                    self.label.setHidden(False)
                else:
                    self.label.setHidden(True)
                self.kolor = 4
                QTest.qWait(random.randint(1000, 3000))
                QSound.play("dingdd.wav")
                self.time_start = time.time()

            elif self.kolor == 4 and self.krok < 7:
                self.time_stop = time.time()
                self.czas = (self.time_stop-self.time_start)*1000
                self.krok += 1
                self.kroki.setText("próba {}/3".format(str(self.krok-4)))
                self.wynik.setText("Wynik = {}".format(str(self.czas)[:5]))

                self.label.setText("Naciśnij ENTER")
                self.label.setHidden(False)
                self.kolor = 3

            if self.krok == 7:
                QTest.qWait(3000)
                self.backClicked.emit()


ad()


class TestScreen(QWidget):
    backClicked = pyqtSignal()
    resultClicked = pyqtSignal()
    wyniki_wizualne = []
    wyniki_sluchowe = []

    def __init__(self):
        super(TestScreen, self).__init__()
        self.time_start = 0
        self.time_stop = 0
        self.czas = 0
        self.square = QFrame(self)
        self.col = QColor(255, 0, 0)
        self.font = QFont('times', 13)
        self.czy_tekst = True

        self.wyniki_wizualne = []
        self.wyniki_sluchowe = []

        self.label = QLabel(self)
        self.info = QLabel(self)
        self.wynik = QLabel(self)
        self.kroki = QLabel(self)

        self.back = QPushButton('Back', self)
        self.back.setGeometry(QRect(30, 30, 60, 20))
        self.back.clicked.connect(self.back_clicked)

        self.krok = 0
        self.kolor = 1
        self.rysuj()
        self.prepare_labels()

    def back_clicked(self):
        self.backClicked.emit()
        self.label.setText("Aby zacząć Demo - wciśnij Enter")

    def prepare_labels(self):

        self.label.setText("Aby zacząć Demo - wciśnij Enter")
        self.label.setFont(self.font)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setGeometry(QRect(20, -20, 400, 170))

        self.wynik.setFont(self.font)
        self.wynik.setGeometry(QRect(10, 300, 400, 170))
        self.wynik.setHidden(True)

        self.info.setFont(self.font)
        self.info.setGeometry(QRect(120, 200, 400, 170))
        self.info.setHidden(True)

        self.kroki.setFont(self.font)
        self.kroki.setGeometry(QRect(350, 300, 400, 170))
        self.kroki.setText("próba {}/3".format(str(self.krok)))

    def rysuj(self):
        self.square.setGeometry(90, 100, 250, 250)
        self.square.setStyleSheet("QWidget { background-color: %s }" % self.col.name())

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter-1:
            if self.kolor == 1 and self.krok < 3:
                if self.czy_tekst:
                    self.label.setText("Gdy kolor będzie zielony\nnaciśnij Enter")
                    self.czy_tekst = False
                    self.label.setHidden(False)
                else:
                    self.label.setHidden(True)
                self.kolor = 2
                QTest.qWait(random.randint(1000, 3000))
                self.col.setRgb(0, 255, 0)
                self.square.setStyleSheet("QFrame { background-color: %s }" % self.col.name())
                self.time_start = time.time()

            elif self.kolor == 2 and self.krok < 3:
                self.time_stop = time.time()
                self.czas = (self.time_stop-self.time_start)*1000
                self.wyniki_wizualne.append(self.czas)
                self.krok += 1
                self.kroki.setText("próba {}/3".format(str(self.krok)))
                self.wynik.setText("Wynik = {}".format(str(self.czas)[:5]))

                QTest.qWait(200)
                self.col.setRgb(255, 0, 0)
                self.square.setStyleSheet("QFrame { background-color: %s }" % self.col.name())
                self.label.setText("Naciśnij ENTER")
                self.label.setHidden(False)
                self.kolor = 1

            if self.krok == 3:
                self.square.repaint()
                self.square.setHidden(True)
                self.krok += 1
                self.czy_tekst = True
                self.kolor = 3
                self.kroki.setText("próba {}/3".format(0))
                self.label.setText("Test dźwiękowy - Naciśnij Enter")

            elif self.kolor == 3 and self.krok < 7:
                if self.czy_tekst:
                    self.czy_tekst = False
                    self.label.setText("Gdy usłyszysz dźwięk\nnaciśnij Enter")
                    self.label.setHidden(False)
                else:
                    self.label.setHidden(True)
                self.kolor = 4
                QTest.qWait(random.randint(1000, 3000))
                QSound.play("dingdd.wav")
                self.time_start = time.time()

            elif self.kolor == 4 and self.krok < 7:
                self.time_stop = time.time()
                self.czas = (self.time_stop-self.time_start)*1000
                self.wyniki_wizualne.append(self.czas)
                self.krok += 1
                self.kroki.setText("próba {}/3".format(str(self.krok-4)))
                self.wynik.setText("Wynik = {}".format(str(self.czas)[:5]))

                self.label.setText("Naciśnij ENTER")
                self.label.setHidden(False)
                self.kolor = 3

            if self.krok == 7:
                QTest.qWait(1000)
                self.resultClicked.emit()


class ResultScreen(QWidget):
    backClicked = pyqtSignal()

    def __init__(self):
        super(ResultScreen, self).__init__()

        self.font = QFont('times', 13)
        self.back = QPushButton('Back', self)
        self.back.setGeometry(QRect(30, 30, 60, 20))
        self.back.clicked.connect(self.back_clicked)

        self.label_wz = QLabel("Wzrokowe", self)
        self.label_wz.setGeometry(QRect(30, 30, 400, 170))
        self.label_wz.setFont(QFont('times', 13))

        self.label1 = QLabel(self)
        self.label1.setGeometry(QRect(30, 60, 400, 170))
        self.label2 = QLabel(self)
        self.label2.setGeometry(QRect(30, 90, 400, 170))
        self.label3 = QLabel(self)
        self.label3.setGeometry(QRect(30, 120, 400, 170))

        self.label_sl = QLabel("Słuchowe", self)
        self.label_sl.setGeometry(QRect(120, 30, 400, 170))
        self.label_sl.setFont(QFont('times', 13))

        self.label4 = QLabel(self)
        self.label4.setGeometry(QRect(120, 60, 400, 170))
        self.label5 = QLabel(self)
        self.label5.setGeometry(QRect(120, 90, 400, 170))
        self.label6 = QLabel(self)
        self.label6.setGeometry(QRect(120, 120, 400, 170))

        self.label_sr = QLabel("Srednie", self)
        self.label_sr.setGeometry(QRect(30, 150, 400, 170))
        self.label_sr.setFont(QFont('times', 13))

        self.label7 = QLabel(self)
        self.label7.setGeometry(QRect(30, 180, 400, 170))
        self.label8 = QLabel(self)
        self.label8.setGeometry(QRect(120, 180, 400, 170))

        self.score()

    def score(self):
        self.label1.setFont(self.font)
        self.label1.setText("{}".format(str(wyyniki[0])))
        self.label2.setFont(self.font)
        self.label2.setText("{}".format(str(wyyniki[1])))
        self.label3.setFont(self.font)
        self.label3.setText("{}".format(str(wyyniki[2])))

        self.label4.setFont(self.font)
        self.label4.setText("{}".format(str(wyyniki[3])))
        self.label5.setFont(self.font)
        self.label5.setText("{}".format(str(wyyniki[4])))
        self.label6.setFont(self.font)
        self.label6.setText("{}".format(str(wyyniki[5])))

        srednia1 = sum(wyyniki[:3])/3
        srednia2 = sum(wyyniki[3:])/3

        self.label7.setFont(self.font)
        self.label7.setText("{}".format(str(srednia1)[:6]))
        self.label8.setFont(self.font)
        self.label8.setText("{}".format(str(srednia2)[:6]))

    def back_clicked(self):
        self.backClicked.emit()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow(None)
    window.show()
    sys.exit(app.exec_())
