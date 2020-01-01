from pytz import timezone
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
import requests

# ラジオゾンデ観測データ(Wyoming大学; text形式)の先頭スキップ数
SKIP_LINE_SONDE_TXT    = 4
# ラジオゾンデ観測データ(Wyoming大学; text形式)の1行のカラム数
N_COLUMN_SONDE_TXT     = 11
# ラジオゾンデ観測データ(Wyoming大学; text形式)の1カラムの文字数
WORDS_COLUMN_SONDE_TXT = 7
# ラジオゾンデ観測データ(tWyoming大学; ext形式)の1行の文字数
WORDS_LINE_SONDE_TXT   = N_COLUMN_SONDE_TXT * WORDS_COLUMN_SONDE_TXT

# ラジオゾンデ観測地点名 - 観測地点番号
SONDE_STATION = {
    'wakkanai'       : '47401',
    'sapporo'        : '47412',
    'kushiro'        : '47418',
    'akita'          : '47582',
    'wajima'         : '47600',
    'tateno'         : '47646',
    'hachijyojima'   : '47678',
    'matsue'         : '47741',
    'shionomisaki'   : '47778',
    'fukuoka'        : '47807',
    'kagoshima'      : '47827',
    'naze'           : '47909',
    'ishigakijima'   : '47918',
    'minamidaitojima': '47945',
    'chichijima'     : '47971',
    'minamitorishima': '47991'
}


class SondeData:
    """
    @brief:
      ラジオゾンデ観測データの構造体(structure of ndarrays)
    """
    pass


def get_latest_obs_time() -> tuple:
    """
    @brief:
      最新データの観測時刻(UTC)を取得します
    """
    # 現在時刻をUTCで取得
    utc_now = datetime.now(timezone('UTC'))

    # 最新データの観測時刻を算定 (現在時刻を最新の00Zまたは12Zに変換)
    if 3 <= utc_now.hour < 15:
        # 00Z
        utc_obs = utc_now.replace(hour=0, minute=0, second=0, microsecond=0)
    elif 15 <= utc_now.hour <= 24:
        # 12Z
        utc_obs = utc_now.replace(hour=12, minute=0, second=0, microsecond=0)
    else:  # 0 <= utc_now.hour < 3
        # 12Z
        utc_obs = utc_now.replace(hour=12, minute=0, second=0, microsecond=0) - datetime.timedelta(days=1)

    # 観測年
    year = utc_obs.strftime("%Y")

    # 観測月
    month = utc_obs.strftime("%m").lstrip("0")

    # 観測日
    day = utc_obs.strftime("%d").lstrip("0")

    # 観測時
    hour = utc_obs.strftime("%H")

    # 観測日時
    time = day + hour

    # エコー
    print('[UTC-Time(now)] ' + str(utc_now))
    print('[UTC-Time(obs)] ' + str(utc_obs))

    return year, month, time


def get_emagram_text(station_name: str) -> tuple:
    """
    @brief:
      最新時刻のラジオゾンデ観測データを取得します(text形式)
    """
    # 最新データの観測時刻(UTC)
    year, month, time = get_latest_obs_time()

    # エマグラムのtextデータ(ワイオミング大学)
    url_emagram = 'http://weather.uwyo.edu/cgi-bin/sounding?region=seasia&TYPE=TEXT%3ALIST&YEAR=' \
                  + year + '&MONTH=' + month + '&FROM=' + time + '&TO=' + time \
                  + '&STNM=' + SONDE_STATION[station_name]

    # エコー
    print('[URL          ] ' + url_emagram)

    # Webサイトにgetリクエストで送信し情報を取得
    r = requests.get(url_emagram)

    # HTTPレスポンスボディを取得
    html = r.text

    # BeautifulSoupオブジェクトの生成
    soup = BeautifulSoup(html, 'html.parser')

    # タイトル抽出
    title = soup.find(name='h2').get_text()

    # ラジオゾンデ観測データ取得(最初の<pre>タグ取得)
    data = soup.find(name='pre').get_text()

    # エコー
    print('[Title        ] ' + title)
    print(data)

    return title, data.splitlines()


def parse_emagram_text(title: str, sonde_txt: list) -> SondeData:
    """
    @brief:
      ラジオゾンデ観測データ(text形式)をパースしてndarray形式で保存します
    """
    pres_lst    = []  # 気圧 [hPa]
    height_lst  = []  # 高度 [m]
    temp_lst    = []  # 温度 [C]
    dewtemp_lst = []  # 露点温度 [C]

    for i_line, s_line in enumerate(sonde_txt):
        # 先頭行スキップ
        if i_line <= SKIP_LINE_SONDE_TXT:
            continue
        # 空行スキップ
        if len(s_line) <= 0:
            continue
        # 文字数が異なる場合はエラー
        if len(s_line) != WORDS_LINE_SONDE_TXT:
            raise

        # パース
        idx_st = 0
        data_tmp = []
        for i in range(N_COLUMN_SONDE_TXT):
            idx_en = idx_st + WORDS_COLUMN_SONDE_TXT
            data_tmp.append(s_line[idx_st:idx_en])
            idx_st += WORDS_COLUMN_SONDE_TXT

        # リストに追加
        if len(data_tmp[0].strip()) > 0:
            pres_lst.append(float(data_tmp[0]))
        if len(data_tmp[1].strip()) > 0:
            height_lst.append(float(data_tmp[1]))
        if len(data_tmp[2].strip()) > 0:
            temp_lst.append(float(data_tmp[2]))
        if len(data_tmp[3].strip()) > 0:
            dewtemp_lst.append(float(data_tmp[3]))

    # python list => numpy ndarray
    sonde_data = SondeData()
    sonde_data.title   = title.strip()
    sonde_data.pres    = np.array(pres_lst, dtype=np.float64)
    sonde_data.height  = np.array(height_lst, dtype=np.float64)
    sonde_data.temp    = np.array(temp_lst, dtype=np.float64)
    sonde_data.dewtemp = np.array(dewtemp_lst, dtype=np.float64)

    return sonde_data


def plot_emagram(sonde_data: SondeData) -> None:
    """
    @brief:
      ラジオゾンデ観測データ(ndarray形式)からエマグラムを作成します
    """
    fig, ax = plt.subplots()

    ax.plot(sonde_data.temp   , sonde_data.pres[0:len(sonde_data.temp)]   ,
            color='k', linestyle='solid' , linewidth=2, label='temperature'          )
    ax.plot(sonde_data.dewtemp, sonde_data.pres[0:len(sonde_data.dewtemp)],
            color='k', linestyle='dashed', linewidth=2, label='dew point temperature')

    plt.title(sonde_data.title, fontsize=12)
    plt.xlabel('Temperature [C]', fontsize=12)
    plt.ylabel('Pressure [hPa]', fontsize=12)
    ax.invert_yaxis()
    plt.legend(loc='best')

    plt.show()


if __name__ == '__main__':
    print("++++++++++ pyema (Emagram tools for python) ++++++++++")
    print()

    #for name in ['sapporo', 'wajima', 'tateno', 'kagoshima']:
    for name in ['tateno']:
        # 最新のラジオゾンデ観測データ取得(text形式)
        title, sonde_txt = get_emagram_text(name)

        # ラジオゾンデ観測データ(text形式)をパースしてndarray形式で保存
        sonde_data = parse_emagram_text(title, sonde_txt)

        # ラジオゾンデ観測データ(ndarray形式)からエマグラムを作成
        plot_emagram(sonde_data)
