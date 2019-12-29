import numpy as np
from bs4 import BeautifulSoup
import requests


def get_emagram_text() -> list:
    # 取得年
    year = 2019

    # 取得月
    month = 12

    # 取得日時(UTC)
    time = 2912

    # 観測地点番号
    station = 47646  # 館野

    # エマグラムのtextデータ(ワイオミング大学)
    url_emagram = 'http://weather.uwyo.edu/cgi-bin/sounding?region=seasia&TYPE=TEXT%3ALIST&YEAR=' \
                  + str(year) + '&MONTH=' + str(month) + '&FROM=' + str(time) + '&TO=' + str(time) \
                  + '&STNM=' + str(station)

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
    print('[URL]   ' + url_emagram)
    print('[Title] ' + title)
    print(data)

    return data.splitlines()


if __name__ == '__main__':
    print("++++++++++ pyema (Emagram tools for python) ++++++++++")
    print()

    # ラジオゾンデ観測データ取得(text形式)
    sonde_txt = get_emagram_text()
