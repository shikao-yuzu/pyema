import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout, QMessageBox, \
                            QLabel, QLineEdit, QPushButton, QAction, QComboBox
from PyQt5.QtCore import pyqtSlot
import pyema


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # window
        self.title = 'pyema'
        #self.left   = 100
        #self.top    = 100
        #self.width  = 240
        #self.height = 240

        self.__init_ui()

    def __init_ui(self) -> None:
        # メニュー
        menu = self.menuBar()

        # メニュー: File
        menu_file = menu.addMenu('File')

        # メニュー: File - Exit
        menu_file_exit = QAction('Exit', self)
        menu_file_exit.triggered.connect(self.close)
        menu_file.addAction(menu_file_exit)

        # Mainウィジェット
        main_widget = PyemaGUI()

        # ウィジェット設定
        self.setCentralWidget(main_widget)

        # ウインドウ
        self.setWindowTitle(self.title)
        #self.setGeometry(self.left, self.top, self.width, self.height)


class PyemaGUI(QWidget):
    # ラジオゾンデ観測地点名 - 観測地点番号
    SONDE_STATION = {
        '稚内(47401)'    : '47401',
        '札幌(47412)'    : '47412',
        '釧路(47418)'    : '47418',
        '秋田(47582)'    : '47582',
        '輪島(47600)'    : '47600',
        '館野(47646)'    : '47646',
        '八丈島(47678)'  : '47678',
        '松江(47741)'    : '47741',
        '潮岬(47778)'    : '47778',
        '福岡(47807)'    : '47807',
        '鹿児島(47827)'  : '47827',
        '名瀬(47909)'    : '47909',
        '石垣島(47918)'  : '47918',
        '南大東島(47945)': '47945',
        '父島(47971)'    : '47971',
        '南鳥島(47991)'  : '47991'
    }

    def __init__(self):
        super().__init__()

        # pyema parameter
        self.obs_time = 'latest'

        self.__init_ui()

    def __init_ui(self) -> None:
        # ウィジェット配置: 格子状
        grid = QGridLayout()
        grid.setSpacing(10)

        # 観測地点名
        self.combo_station = QComboBox(self)
        self.combo_station.addItem('稚内(47401)'       )
        self.combo_station.addItem('札幌(47412)'       )
        self.combo_station.addItem('釧路(47418)'       )
        self.combo_station.addItem('秋田(47582)'       )
        self.combo_station.addItem('輪島(47600)'       )
        self.combo_station.addItem('館野(47646)'       )
        self.combo_station.addItem('八丈島(47678)'     )
        self.combo_station.addItem('松江(47741)'       )
        self.combo_station.addItem('潮岬(47778)'       )
        self.combo_station.addItem('福岡(47807)'       )
        self.combo_station.addItem('鹿児島(47827)'     )
        self.combo_station.addItem('名瀬(47909)'       )
        self.combo_station.addItem('石垣島(47918)'     )
        self.combo_station.addItem('南大東島(47945)'   )
        self.combo_station.addItem('父島(47971)'       )
        self.combo_station.addItem('南鳥島(47991)'     )
        self.combo_station.addItem('...地点番号で指定' )
        self.combo_station.resize(self.combo_station.sizeHint())

        # 観測地点番号
        self.text_station = QLineEdit(self)

        # プロット図表示
        button_plot = QPushButton('plot', self)
        button_plot.clicked.connect(self.__on_click_plot)

        # ウィジェット設定
        grid.addWidget(QLabel('観測地点')      , 1, 0)
        grid.addWidget(QLabel('地点名')        , 1, 1)
        grid.addWidget(self.combo_station      , 1, 2)

        grid.addWidget(QLabel('地点番号')      , 2, 1)
        grid.addWidget(self.text_station       , 2, 2)

        grid.addWidget(QLabel('観測時刻')      , 3, 0)
        grid.addWidget(QLabel('最新')          , 3, 1)

        grid.addWidget(QLabel('プロット図表示'), 4, 0)
        grid.addWidget(button_plot             , 4, 1)

        self.setLayout(grid)

    @pyqtSlot()
    def __on_click_plot(self):
        try:
            if self.combo_station.currentText() == '...地点番号で指定':
                station = self.text_station.text()
            else:
                station = self.SONDE_STATION[self.combo_station.currentText()]

            pyema.run_pyema(station, self.obs_time)

        except Exception as e:
            import traceback
            except_str = traceback.format_exc()
            QMessageBox.critical(self, "Error", except_str, QMessageBox.Yes)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
