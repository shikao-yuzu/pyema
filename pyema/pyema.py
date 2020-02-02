# TODO: use pandas
# TODO: 表機能
# TODO: ワイオミング大のpdfをそのまま表示
# TODO: 乾燥断熱線，湿潤断熱線, LCL
import numpy as np
import japanize_matplotlib
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
import requests
import pyema_util

# ラジオゾンデ観測データ(Wyoming大学; text形式)の先頭スキップ数
SKIP_LINE_SONDE_TXT    = 4
# ラジオゾンデ観測データ(Wyoming大学; text形式)の1行のカラム数
N_COLUMN_SONDE_TXT     = 11
# ラジオゾンデ観測データ(Wyoming大学; text形式)の1カラムの文字数
WORDS_COLUMN_SONDE_TXT = 7
# ラジオゾンデ観測データ(tWyoming大学; ext形式)の1行の文字数
WORDS_LINE_SONDE_TXT   = N_COLUMN_SONDE_TXT * WORDS_COLUMN_SONDE_TXT


class SondeData:
    """
    @brief:
      ラジオゾンデ観測データの構造体(structure of ndarrays)
    """
    pass


def __get_emagram_text(station: str, obs_time: str) -> tuple:
    """
    @brief:
      ラジオゾンデ観測データを取得します(text形式)
    """
    # エマグラムのtextデータ(ワイオミング大学)
    url_emagram = 'http://weather.uwyo.edu/cgi-bin/sounding?region=seasia&TYPE=TEXT%3ALIST&YEAR=' \
                  + obs_time['year'] + '&MONTH=' + obs_time['month'] + '&FROM=' + obs_time['time'] \
                  + '&TO=' + obs_time['time'] + '&STNM=' + station

    # エコー
    print('[URL        ] ' + url_emagram)

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
    print('[Title      ] ' + title)
    print(data)

    return title, data.splitlines()


def __parse_emagram_text(title: str, sonde_txt: list) -> SondeData:
    """
    @brief:
      ラジオゾンデ観測データ(text形式)をパースしてndarray形式で保存します
    """
    pres_lst    = []  # 気圧 [hPa]
    height_lst  = []  # 高度 [m]
    temp_lst    = []  # 温度 [C]
    dewtemp_lst = []  # 露点温度 [C]
    theta_lst   = []  # 温位 [K]
    theta_e_lst = []  # 相当温位 [K]
    vtheta_lst  = []  # 仮温位 [K]

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
        if len(data_tmp[8].strip()) > 0:
            theta_lst.append(float(data_tmp[8]))
        if len(data_tmp[9].strip()) > 0:
            theta_e_lst.append(float(data_tmp[9]))
        if len(data_tmp[10].strip()) > 0:
            vtheta_lst.append(float(data_tmp[10]))

    # python list => numpy ndarray
    sonde_data = SondeData()
    sonde_data.title   = title.strip()
    sonde_data.pres    = np.array(pres_lst   , dtype=np.float64)
    sonde_data.height  = np.array(height_lst , dtype=np.float64)
    sonde_data.temp    = np.array(temp_lst   , dtype=np.float64)
    sonde_data.dewtemp = np.array(dewtemp_lst, dtype=np.float64)
    sonde_data.theta   = np.array(theta_lst  , dtype=np.float64)
    sonde_data.theta_e = np.array(theta_e_lst, dtype=np.float64)
    sonde_data.vtheta  = np.array(vtheta_lst , dtype=np.float64)

    return sonde_data


def __plot_emagram(sonde_data: SondeData, param: dict) -> None:
    """
    @brief:
      ラジオゾンデ観測データ(ndarray形式)からエマグラムを図化します
    """
    if   param['axis_h']['type'] == 't':
        # 図化
        __plot_emagram_temperature(sonde_data, param)
    elif param['axis_h']['type'] == 'pt':
        # 飽和相当温位算出
        __calc_theta_es(sonde_data)
        # 図化
        __plot_emagram_theta(sonde_data, param)
    else:
        raise


def __plot_emagram_temperature(sonde_data: SondeData, param: dict) -> None:
    """
    @brief:
      ラジオゾンデ観測データ(ndarray形式)からエマグラムを図化します
    """
    fig, ax = plt.subplots()

    if   param['axis_v']['type'] == 'p':
        ax.plot(sonde_data.temp   , sonde_data.pres[0:len(sonde_data.temp)   ],
                color='k', linestyle='solid' , linewidth=2, label='気温'    )
        ax.plot(sonde_data.dewtemp, sonde_data.pres[0:len(sonde_data.dewtemp)],
                color='b', linestyle='dashed', linewidth=2, label='露点温度')
        plt.ylabel('気圧 [hPa]', fontsize=12)
        ax.invert_yaxis()
    elif param['axis_v']['type'] == 'z':
        ax.plot(sonde_data.temp   , sonde_data.height[0:len(sonde_data.temp)   ],
                color='k', linestyle='solid' , linewidth=2, label='気温'    )
        ax.plot(sonde_data.dewtemp, sonde_data.height[0:len(sonde_data.dewtemp)],
                color='b', linestyle='dashed', linewidth=2, label='露点温度')
        plt.ylabel('高度 [m]', fontsize=12)
    else:
        raise

    plt.title(sonde_data.title  , fontsize=12)
    plt.xlabel('気温 [C]', fontsize=12)

    ax.set_xlim(param['axis_h']['limit'])
    ax.set_ylim(param['axis_v']['limit'])

    plt.grid(color='gray', ls=':')
    plt.legend(loc='best')
    plt.show()


def __plot_emagram_theta(sonde_data: SondeData, param: dict) -> None:
    """
    @brief:
      ラジオゾンデ観測データ(ndarray形式)から温位エマグラムを図化します
    """
    fig, ax = plt.subplots()

    if   param['axis_v']['type'] == 'p':
        ax.plot(sonde_data.theta   , sonde_data.pres[0:len(sonde_data.temp)    ],
                color='k', linestyle='solid' , linewidth=2, label='温位'        )
        ax.plot(sonde_data.theta_e , sonde_data.pres[0:len(sonde_data.theta_e) ],
                color='b', linestyle='dashed', linewidth=2, label='相当温位'    )
        ax.plot(sonde_data.theta_es, sonde_data.pres[0:len(sonde_data.theta_es)],
                color='r', linestyle='dotted', linewidth=2, label='飽和相当温位')
        plt.ylabel('気圧 [hPa]', fontsize=12)
        ax.invert_yaxis()
    elif param['axis_v']['type'] == 'z':
        ax.plot(sonde_data.theta   , sonde_data.height[0:len(sonde_data.temp)    ],
                color='k', linestyle='solid' , linewidth=2, label='温位'        )
        ax.plot(sonde_data.theta_e , sonde_data.height[0:len(sonde_data.theta_e) ],
                color='b', linestyle='dashed', linewidth=2, label='相当温位'    )
        ax.plot(sonde_data.theta_es, sonde_data.height[0:len(sonde_data.theta_es)],
                color='r', linestyle='dotted', linewidth=2, label='飽和相当温位')
        plt.ylabel('高度 [m]', fontsize=12)
    else:
        raise

    plt.title(sonde_data.title, fontsize=12)
    plt.xlabel('温位 [K]', fontsize=12)

    ax.set_xlim(param['axis_h']['limit'])
    ax.set_ylim(param['axis_v']['limit'])

    plt.grid(color='gray', ls=':')
    plt.legend(loc='best')
    plt.show()


def __calc_theta_es(sonde_data: SondeData):
    """
    @brief:
      飽和相当温位θe*(t,p)[K]を求めます
    """
    # 絶対温度 [K]
    t = sonde_data.temp[0:len(sonde_data.theta_e)] + 273.15

    # 気圧 [hPa]
    p = sonde_data.pres[0:len(sonde_data.theta_e)]

    # 飽和相当温位 [K]
    sonde_data.theta_es = pyema_util.calc_theta_es(t, p)


def run_pyema(param: dict):
    """
    @brief:
      main関数
    """
    try:
        # ラジオゾンデ観測データ取得(text形式)
        title, sonde_txt = __get_emagram_text(param['station'], param['obs_time'])

        # ラジオゾンデ観測データ(text形式)をパースしてndarray形式で保存
        sonde_data = __parse_emagram_text(title, sonde_txt)

        # ラジオゾンデ観測データ(ndarray形式)からエマグラムを図化
        __plot_emagram(sonde_data, param)

    except Exception as e:
        raise e


if __name__ == '__main__':
    print("++++++++++ pyema (Emagram tools for python) ++++++++++")
    print()

    param = {
        'station' : '47646',
        'obs_time': {
            'year' : '2020',
            'month': '2'   ,
            'time' : '100'
        },
        'axis_h': {
            'type': 'pt',
            'limit': None,
        },
        'axis_v': {
            'type': 'p',
            'limit': None
        }
    }

    run_pyema(param)
