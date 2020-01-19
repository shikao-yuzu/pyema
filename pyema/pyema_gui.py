import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit, QPushButton, QMessageBox, QAction
from PyQt5.QtCore import pyqtSlot
import pyema


class App(QMainWindow):
    def __init__(self):
        super().__init__()

        self.title = "pyema"

        self.left   = 100
        self.top    = 100
        self.width  = 240
        self.height = 240

        self.initUI()

    def initUI(self) -> None:
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.statusBar().showMessage("created by shikao-yuzu")

        # Menu
        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu("File")

        exitButton = QAction("Exit", self)
        exitButton.setStatusTip("Exit application")
        exitButton.triggered.connect(self.close)
        fileMenu.addAction(exitButton)

        # Create button
        button = QPushButton("pyema", self)
        button.setToolTip("This is an example button")
        button.move(10,30)
        button.clicked.connect(self.on_click)

        self.show()

    @pyqtSlot()
    def on_click(self):
        pyema.run_pyema('tateno', 'latest')


def main() -> None:
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
