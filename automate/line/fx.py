from line_notify_bot import LINENotifyBot
import sys

import config


""" send weight with graph

Using Line notify API, send weight and graph
https://notify-bot.line.me/ja/

ACCESS_TOKEN is a secret key given by Line

"""

ACCESS_TOKEN = config.ACCESS_TOKEN

bot = LINENotifyBot(access_token=ACCESS_TOKEN)

bot.send(
    message = sys.argv[1],
    image = sys.argv[2],  # png or jpg
    )
