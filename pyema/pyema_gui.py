from pytz import timezone
from datetime import datetime, timedelta
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout, QMessageBox, \
                            QLabel, QLineEdit, QPushButton, QAction, QComboBox
from PyQt5.QtCore import pyqtSlot
import pyema


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.__init_ui()

    def __init_ui(self) -> None:
        # タイトル
        self.title = 'pyema: エマグラム表示ツール'

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

        # ウィジェット設定
        self.__set_widget()

        # グリッド設定
        self.__set_grid()

    def __set_widget(self) -> None:
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

        # 観測時刻：最新観測時刻取得
        self.button_obs_time_now = QPushButton('最新観測時刻を取得', self)
        self.button_obs_time_now.clicked.connect(self.__on_click_obs_time_now)

        # 観測時刻: 年
        self.text_obs_time_y = QLineEdit(self)

        # 観測時刻: 月
        self.text_obs_time_m = QLineEdit(self)

        # 観測時刻: 日
        self.text_obs_time_d = QLineEdit(self)

        # 観測時刻: 時
        self.combo_obs_time_h = QComboBox(self)
        self.combo_obs_time_h.addItem('00Z')
        self.combo_obs_time_h.addItem('12Z')
        self.combo_obs_time_h.resize(self.combo_obs_time_h.sizeHint())

        # 横軸設定
        self.combo_axis_h = QComboBox(self)
        self.combo_axis_h.addItem('気温[C]')
        self.combo_axis_h.addItem('温位[K]')
        self.combo_axis_h.resize(self.combo_station.sizeHint())

        # 縦軸設定
        self.combo_axis_v = QComboBox(self)
        self.combo_axis_v.addItem('気圧[hPa]')
        self.combo_axis_v.addItem('高度[m]')
        self.combo_axis_v.resize(self.combo_station.sizeHint())

        # プロット図表示
        self.button_plot = QPushButton('plot (matplotlib)', self)
        self.button_plot.clicked.connect(self.__on_click_plot)

    def __set_grid(self) -> None:
        # ウィジェット配置方法: 格子状
        grid = QGridLayout()
        grid.setSpacing(10)

        # ウィジェットをグリッドに設定
        irow = 1
        grid.addWidget(QLabel('観測地点')      , irow, 0)
        grid.addWidget(QLabel('地点名')        , irow, 1)
        grid.addWidget(self.combo_station      , irow, 2)

        irow += 1
        grid.addWidget(QLabel('地点番号')      , irow, 1)
        grid.addWidget(self.text_station       , irow, 2)

        irow += 1
        grid.addWidget(QLabel('観測時刻(UTC)') , irow, 0)
        grid.addWidget(self.button_obs_time_now, irow, 1, 1, 2)

        irow += 1
        grid.addWidget(QLabel('年(yyyy)')      , irow, 1)
        grid.addWidget(self.text_obs_time_y    , irow, 2)

        irow += 1
        grid.addWidget(QLabel('月(mm)')        , irow, 1)
        grid.addWidget(self.text_obs_time_m    , irow, 2)

        irow += 1
        grid.addWidget(QLabel('日(dd)')        , irow, 1)
        grid.addWidget(self.text_obs_time_d    , irow, 2)

        irow += 1
        grid.addWidget(QLabel('時(hh)')        , irow, 1)
        grid.addWidget(self.combo_obs_time_h   , irow, 2)

        irow += 1
        grid.addWidget(QLabel('横軸')          , irow, 0)
        grid.addWidget(self.combo_axis_h       , irow, 1)

        irow += 1
        grid.addWidget(QLabel('縦軸')          , irow, 0)
        grid.addWidget(self.combo_axis_v       , irow, 1)

        irow += 1
        grid.addWidget(QLabel('プロット図表示'), irow, 0)
        grid.addWidget(self.button_plot        , irow, 1, 1, 2)

        self.setLayout(grid)

    @pyqtSlot()
    def __on_click_plot(self):
        try:
            # 観測地点設定
            if self.combo_station.currentText() == '...地点番号で指定':
                station = self.text_station.text()
            else:
                station = self.SONDE_STATION[self.combo_station.currentText()]

            # 観測時刻設定
            year  = self.text_obs_time_y.text()
            month = self.text_obs_time_m.text().lstrip('0')
            time  = self.text_obs_time_d.text().lstrip('0') \
                  + self.combo_obs_time_h.currentText().rstrip('Z')

            # 横軸設定
            if   self.combo_axis_h.currentText() == '気温[C]':
                value_h = 't'
            elif self.combo_axis_h.currentText() == '温位[K]':
                value_h = 'pt'
            else:
                raise

            # 縦軸設定
            if   self.combo_axis_v.currentText() == '気圧[hPa]':
                value_v = 'p'
            elif self.combo_axis_v.currentText() == '高度[m]':
                value_v = 'z'
            else:
                raise

            # パラメータ設定
            param = {
                'station' : station,
                'obs_time': {
                    'year' : year,
                    'month': month,
                    'time' : time
                },
                'value_h' : value_h,
                'value_v' : value_v
            }

            pyema.run_pyema(param)

        except Exception as e:
            import traceback
            except_str = traceback.format_exc()
            QMessageBox.critical(self, "Error", except_str, QMessageBox.Yes)

    @pyqtSlot()
    def __on_click_obs_time_now(self):
        year, month, day, hour = PyemaGUI.get_latest_obs_time()
        self.text_obs_time_y.setText(year)
        self.text_obs_time_m.setText(month)
        self.text_obs_time_d.setText(day)
        self.combo_obs_time_h.setCurrentText(hour)

    @staticmethod
    def get_latest_obs_time() -> tuple:
        """
        @brief:
          最新データの観測時刻(UTC)を取得します
        """
        # 現在時刻をUTCで取得
        utc_now = datetime.now(timezone('UTC'))

        # 最新データの観測時刻を算定 (現在時刻を最新の00Zまたは12Zに変換)
        if    3 <= utc_now.hour <  15:
            # 00Z
            utc_obs = utc_now.replace(hour=0, minute=0, second=0, microsecond=0)
        elif 15 <= utc_now.hour <= 24:
            # 12Z
            utc_obs = utc_now.replace(hour=12, minute=0, second=0, microsecond=0)
        else:  # 0 <= utc_now.hour < 3
            # 12Z
            utc_obs = utc_now.replace(hour=12, minute=0, second=0, microsecond=0) - timedelta(days=1)

        year  = utc_obs.strftime("%Y")        # 観測年
        month = utc_obs.strftime("%m")        # 観測月
        day   = utc_obs.strftime("%d")        # 観測日
        hour  = utc_obs.strftime("%H") + 'Z'  # 観測時

        # エコー
        print('[UTC(   now)] ' + str(utc_now))
        print('[UTC(latest)] ' + str(utc_obs))

        return year, month, day, hour


if __name__ == '__main__':
    app    = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
