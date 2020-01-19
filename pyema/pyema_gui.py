import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QAction, QComboBox
from PyQt5.QtCore import pyqtSlot
import pyema


class App(QMainWindow):
    def __init__(self):
        super().__init__()

        # window
        self.title = 'pyema'
        self.left   = 100
        self.top    = 100
        self.width  = 240
        self.height = 240

        # pyema parameter
        self.obs_time = 'latest'

        self.__init_ui()

    def __init_ui(self) -> None:
        # ウインドウ
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        # メニュー: File
        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu('File')

        # メニュー: File - Exit
        exitButton = QAction('Exit', self)
        exitButton.setStatusTip('Exit application')
        exitButton.triggered.connect(self.close)
        fileMenu.addAction(exitButton)

        # コンボボックス
        self.combo_station = QComboBox(self)
        self.combo_station.addItem('tateno')
        self.combo_station.addItem('wakkanai')
        self.combo_station.addItem('sapporo')
        self.combo_station.addItem('kushiro')
        self.combo_station.addItem('akita')
        self.combo_station.addItem('wajima')
        self.combo_station.addItem('hachijyojima')
        self.combo_station.addItem('matsue')
        self.combo_station.addItem('shionomisaki')
        self.combo_station.addItem('fukuoka')
        self.combo_station.addItem('kagoshima')
        self.combo_station.addItem('naze')
        self.combo_station.addItem('ishigakijima')
        self.combo_station.addItem('minamidaitojima')
        self.combo_station.addItem('chichijima')
        self.combo_station.addItem('minamitorishima')
        self.combo_station.resize(self.combo_station.sizeHint())
        self.combo_station.move(10, 30)

        # ボタン: plot
        button = QPushButton('plot', self)
        button.setToolTip('run pyema')
        button.move(10, 100)
        button.clicked.connect(self.__on_click_plot)

        self.show()

    @pyqtSlot()
    def __on_click_plot(self):
        pyema.run_pyema(self.combo_station.currentText(), self.obs_time)


def main() -> None:
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
