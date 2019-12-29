import os
import csv
import re
import datetime
from bs4 import BeautifulSoup
import requests
import jaconv


# 取得対象のWebサイト
URL_ANTLERS_CAL = 'http://www.so-net.ne.jp/antlers/games'

# 出力ファイル名
OUTPUT_PATH = 'antlers.csv'

# 年
YEAR_NOW = '2019'


def output_game_schedule(soup: BeautifulSoup, competitions: list, idx_comp: int) -> None:
    """
    @brief:
      試合情報(HTML)をパースしてGoogleカレンダー用のCSVに出力
    """
    # テーブルの取得
    tables = soup.findAll(name='div', attrs={'class': 'game-index-wrap'})

    # 大会名
    comp = competitions[idx_comp]

    # 試合リスト
    game_lists = tables[idx_comp].findAll(name='div', attrs={'class': 'gameScheduleList__item'})

    # 出力ファイルの再オープン
    csvFile = open(OUTPUT_PATH, 'at', newline = '', encoding = 'shift_jis')
    writer = csv.writer(csvFile)

    # パース＆出力
    try:
        for idx_game, game in enumerate(game_lists):
            # 節
            sec = game.find(name='p', attrs={'class': 'gameScheduleList__season'})
            if sec == None:
                sec = ''
            else:
                sec = sec.get_text().strip()
                sec = jaconv.z2h(sec, kana=False, digit=True, ascii=True)

            # 日
            day = game.find(name='p', attrs={'class': 'gameScheduleList__date'}).get_text().strip()
            day = jaconv.z2h(day, kana=False, digit=True, ascii=True)
            day = re.split('[or +)(※]', day)
            day = day[0].replace('.', '/')

            # 開始時刻
            s_time = game.find(name='p', attrs={'class': 'gameScheduleList__time'}).get_text().strip()

            # 終日イベントフラグと終了時刻の設定
            if s_time == '未定':
                all_day_flag = 'TRUE'
                s_time       = ''
                e_time       = ''
            else:
                all_day_flag = ''
                s_time_dt    = datetime.datetime.strptime(s_time, '%H:%M')
                e_time_dt    = s_time_dt + datetime.timedelta(hours = 2)
                e_time       = e_time_dt.strftime('%H:%M')

            # 対戦相手
            team = game.find(name='span', attrs={'class': 'gameScheduleList__clubName'}).get_text().strip()
            team = jaconv.z2h(team, kana=False, digit=True, ascii=True)

            # スタジアム
            stadium = game.find(name='p', attrs={'class': 'gameScheduleList__stadium'}).get_text().strip()
            stadium = jaconv.z2h(stadium, kana=False, digit=True, ascii=True)
            stadium = stadium.strip('HOME')
            stadium = stadium.strip('AWAY')
            stadium = stadium.strip('\n')

            csvRow = []
            csvRow.append(comp+' '+sec+' '+team)
            csvRow.append(YEAR_NOW+'/'+day)
            csvRow.append(s_time)
            csvRow.append(YEAR_NOW+'/'+day)
            csvRow.append(e_time)
            csvRow.append(all_day_flag)
            csvRow.append('')
            csvRow.append(stadium)

            writer.writerow(csvRow)
    finally:
        csvFile.close()


def main():
    """
    @brief:
      メイン関数
    """
    # Webサイトにgetリクエストで送信し情報を取得
    r = requests.get(URL_ANTLERS_CAL)

    # HTTPレスポンスボディを取得
    html = r.text

    # BeautifulSoupオブジェクトの生成
    soup = BeautifulSoup(html, 'html.parser')

    # 出場大会のリストを構築
    competitions = []
    for c in soup.findAll(name='h3', attrs={'class': 'title -style05_01'}):
        # 全角英数字を半角に変換
        c_z2h = jaconv.z2h(c.string, kana=False, digit=True, ascii=True)

        competitions.append(c_z2h)

    # ヘッダ行のCSV出力
    csvFile = open(OUTPUT_PATH, 'wt', newline = '', encoding = 'shift_jis')
    writer = csv.writer(csvFile)
    try:
        writer.writerow(['Subject', 'Start Date' , 'Start Time', 'End Date', 'End Time', 'All Day Event', 'Description', 'Location'])
    finally:
        csvFile.close()

    # 試合情報のCSV出力
    for idx_comp in range(len(competitions)):
        output_game_schedule(soup, competitions, idx_comp)


if __name__ == '__main__':
    main()
