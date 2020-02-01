from pytz import timezone
from datetime import datetime, timedelta
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout, QMessageBox, \
                            QLabel, QLineEdit, QPushButton, QAction, QComboBox, QFrame
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
        # 観測地点
        self.__set_widget_station()

        # 観測時刻
        self.__set_widget_obs_time()

        # 横軸
        self.__set_widget_axis_h()

        # 縦軸
        self.__set_widget_axis_v()

        # 結果表示
        self.__set_widget_output()

    def __set_widget_station(self) -> None:
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

    def __set_widget_obs_time(self) -> None:
        # 観測時刻：最新観測時刻
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

    def __set_widget_axis_h(self) -> None:
        # 横軸: 種別
        self.combo_axis_h_type = QComboBox(self)
        self.combo_axis_h_type.addItem('気温[C]')
        self.combo_axis_h_type.addItem('温位[K]')
        self.combo_axis_h_type.resize(self.combo_axis_h_type.sizeHint())

        # 横軸: 境界値設定
        self.combo_axis_h_auto = QComboBox(self)
        self.combo_axis_h_auto.addItem('自動')
        self.combo_axis_h_auto.addItem('...ユーザー指定')
        self.combo_axis_h_auto.resize(self.combo_axis_h_auto.sizeHint())

        # 横軸: 左端
        self.text_axis_h1 = QLineEdit(self)

        # 横軸: 右端
        self.text_axis_h2 = QLineEdit(self)

    def __set_widget_axis_v(self) -> None:
        # 縦軸: 種別
        self.combo_axis_v_type = QComboBox(self)
        self.combo_axis_v_type.addItem('気圧[hPa]')
        self.combo_axis_v_type.addItem('高度[m]')
        self.combo_axis_v_type.resize(self.combo_axis_v_type.sizeHint())

        # 縦軸: 境界値設定
        self.combo_axis_v_auto = QComboBox(self)
        self.combo_axis_v_auto.addItem('自動')
        self.combo_axis_v_auto.addItem('...ユーザー指定')
        self.combo_axis_v_auto.resize(self.combo_axis_v_auto.sizeHint())

        # 縦軸: 下端
        self.text_axis_v1 = QLineEdit(self)

        # 縦軸: 上端
        self.text_axis_v2 = QLineEdit(self)

    def __set_widget_output(self) -> None:
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

        # -----------------------------------------------------
        irow += 1
        grid.addWidget(QHLine()                , irow, 0, 1, 3)

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

        # -----------------------------------------------------
        irow += 1
        grid.addWidget(QHLine()                , irow, 0, 1, 3)

        irow += 1
        grid.addWidget(QLabel('横軸設定')      , irow, 0)
        grid.addWidget(QLabel('種別')          , irow, 1)
        grid.addWidget(self.combo_axis_h_type  , irow, 2)

        irow += 1
        grid.addWidget(QLabel('境界値設定')    , irow, 1)
        grid.addWidget(self.combo_axis_h_auto  , irow, 2)

        irow += 1
        grid.addWidget(QLabel('左端')          , irow, 1)
        grid.addWidget(self.text_axis_h1       , irow, 2)

        irow += 1
        grid.addWidget(QLabel('右端')          , irow, 1)
        grid.addWidget(self.text_axis_h2       , irow, 2)

        # -----------------------------------------------------
        irow += 1
        grid.addWidget(QHLine()                , irow, 0, 1, 3)

        irow += 1
        grid.addWidget(QLabel('縦軸設定')      , irow, 0)
        grid.addWidget(QLabel('種別')          , irow, 1)
        grid.addWidget(self.combo_axis_v_type  , irow, 2)

        irow += 1
        grid.addWidget(QLabel('境界値設定')    , irow, 1)
        grid.addWidget(self.combo_axis_v_auto  , irow, 2)

        irow += 1
        grid.addWidget(QLabel('上端')          , irow, 1)
        grid.addWidget(self.text_axis_v2       , irow, 2)

        irow += 1
        grid.addWidget(QLabel('下端')          , irow, 1)
        grid.addWidget(self.text_axis_v1       , irow, 2)

        # -----------------------------------------------------
        irow += 1
        grid.addWidget(QHLine()                , irow, 0, 1, 3)

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
            if   self.combo_axis_h_type.currentText() == '気温[C]':
                axis_h_type = 't'
            elif self.combo_axis_h_type.currentText() == '温位[K]':
                axis_h_type = 'pt'
            else:
                raise

            if   self.combo_axis_h_auto.currentText() == '自動':
                axis_h_limit = None
            else:
                h1 = float(self.text_axis_h1.text())
                h2 = float(self.text_axis_h2.text())
                axis_h_limit = [h1, h2]

            # 縦軸設定
            if   self.combo_axis_v_type.currentText() == '気圧[hPa]':
                axis_v_type = 'p'
            elif self.combo_axis_v_type.currentText() == '高度[m]':
                axis_v_type = 'z'
            else:
                raise

            if   self.combo_axis_v_auto.currentText() == '自動':
                axis_v_limit = None
            else:
                v1 = float(self.text_axis_v1.text())
                v2 = float(self.text_axis_v2.text())
                axis_v_limit = [v1, v2]

            # パラメータ設定
            param = {
                'station' : station,
                'obs_time': {
                    'year' : year,
                    'month': month,
                    'time' : time
                },
                'axis_h' : {
                    'type' : axis_h_type,
                    'limit': axis_h_limit
                },
                'axis_v' : {
                    'type' : axis_v_type,
                    'limit': axis_v_limit
                }
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


class QHLine(QFrame):
    '''
    reference: https://stackoverflow.com/questions/5671354/how-to-programmatically-make-a-horizontal-line-in-qt
    '''
    def __init__(self):
        super(QHLine, self).__init__()
        self.setFrameShape(QFrame.HLine)
        self.setFrameShadow(QFrame.Sunken)


if __name__ == '__main__':
    app    = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
