from line_notify_bot import LINENotifyBot
import sys
import requests
from datetime import datetime, timedelta, timezone
import subprocess
import glob
import logging

import config


""" send weight with graph

Using Line notify API, send weight and graph
https://notify-bot.line.me/ja/

ACCESS_TOKEN is a secret key given by Line

"""


def saveAsPdf(url, dir):
    

    DIR_PATH = dir
    PDF_NAME = 'daily.pdf'
    PATH = DIR_PATH + PDF_NAME

    chunk_size = 2000
    r = requests.get(url, stream=True)

    with open(PATH, 'wb') as fd:
        for chunk in r.iter_content(chunk_size):
            fd.write(chunk)


if __name__ == '__main__':

    # 送信及び、pdf 内に含まれる日付情報について整理する
    JST = timezone(timedelta(hours=+9), 'JST')
    dt_now = datetime.now(JST)

    date = dt_now.strftime('%Y%m%d')

    year_month = dt_now.strftime('%Y%m')
    day = dt_now.strftime('%d')
    day_minus_1 = '0' + str(int(day) - 1)
    date_minus_1 = year_month + day_minus_1[len(day_minus_1)-2:len(day_minus_1)]

    # 会社情報を保存するやつ
    mufg = {
        'name': 'mufg',
        'url': f'https://www.bk.mufg.jp/report/dmr2021/FXDaily{date_minus_1}.pdf'
    }

    smbc = {
        'name': 'smbc',
        'url': f'https://www.smbc.co.jp/market/pdf/fixing{date}.pdf'
    }

    mizuho = {
        'name': 'mizuho',
        'url': f'https://www.mizuhobank.co.jp/market/pdf/daily/dmn210909_1.pdf'
    }


    companies = [mufg, smbc, mizuho]

    """
    毎時間これ実行することにして、時間によって次の内容を分ける
    0 時   ：日付が変わったタイミングで、フォルダ内容削除
    それ以外：フォルダ内にファイルがなければ、データを取得の処理を行う
    """
    
    hour = int(dt_now.strftime('%H'))

    # Cron で実行する際は絶対パスで記述
    isCron = True
    if isCron:
        prefix = '/home/ubuntu/work/fx/'
    else:
        prefix = ''

    logging.basicConfig(filename=prefix+'test.log', level=logging.DEBUG)
    logging.debug(hour)

    for company in companies:
        
        url = company['url']
        name = company['name']

        dir = f'{prefix}{name}/'

        if hour < 3:
            # 前回までのファイルが残っていれば削除する
            subprocess.run(['bash', prefix+'reset_folder.sh', dir])
            continue

        files = glob.glob(dir + '*')
        
        if len(files) > 0:
            continue

        # pdf 形式として保存する
        saveAsPdf(url, dir)

        # linux のコマンドで、pdf -> img の変換を行う
        subprocess.run(['bash', prefix + 'pdf2img.sh', dir])

        # 生成されたファイル（画像）一覧を取得
        files = glob.glob(dir + '*')

        # line notify を使って、画像を送信する
        ACCESS_TOKEN = config.TOKEN

        bot = LINENotifyBot(access_token=ACCESS_TOKEN)

        for file in files:
            print(file)
            bot.send(
                message = f'{name} - {date}',
                image = file,  # png or jpg
                )
