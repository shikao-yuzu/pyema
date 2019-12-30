from pytz import timezone
from datetime import datetime
import numpy as np
from bs4 import BeautifulSoup
import requests


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


def get_emagram_text() -> list:
    """
    @brief:
      最新時刻のラジオゾンデ観測データを取得します(text形式)
    """
    # 最新データの観測時刻(UTC)
    year, month, time = get_latest_obs_time()

    # 観測地点番号
    station = '47646'  # 館野

    # エマグラムのtextデータ(ワイオミング大学)
    url_emagram = 'http://weather.uwyo.edu/cgi-bin/sounding?region=seasia&TYPE=TEXT%3ALIST&YEAR=' \
                  + year + '&MONTH=' + month + '&FROM=' + time + '&TO=' + time \
                  + '&STNM=' + station

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

    return data.splitlines()


if __name__ == '__main__':
    print("++++++++++ pyema (Emagram tools for python) ++++++++++")
    print()

    # 最新のラジオゾンデ観測データ取得(text形式)
    sonde_txt = get_emagram_text()
