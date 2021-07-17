import tweepy
import sys
 
import config


consumer_key = config.API_KEY
consumer_secret = config.API_SECRET_KEY
access_token = config.ACCESS_TOKEN
access_token_secret = config.ACCESS_TOKEN_SECRET
 
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

file_names="./last_10_days_weight.png"#画像が同ディレクトリにある場合
api.update_with_media(filename=file_names,status="テストツイート") 

