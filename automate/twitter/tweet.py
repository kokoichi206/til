import tweepy
import sys
import datetime
import subprocess
from os import system

import config


dt_now = datetime.datetime.now()

consumer_key = config.API_KEY
consumer_secret = config.API_SECRET_KEY
access_token = config.ACCESS_TOKEN
access_token_secret = config.ACCESS_TOKEN_SECRET
 
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

if len(sys.argv) > 1:
	if (dt_now.day % 5) == 0:
		file_names="./last_10_days_weight.png"
		api.update_with_media(filename=file_names,status=sys.argv[1])
		print('API post picture and weight SUCCESS')
	else:
		api.update_status(sys.argv[1])
		print('API post SUCCESS')	
else:
	print('No argument')

