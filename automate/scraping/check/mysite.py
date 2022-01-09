import requests
import time


BaseUrl = "https://kokoichi0206.mydns.jp/"

res = requests.get(BaseUrl).content
headers = {"User-Agent": "Mozilla/5.0"}
res = requests.get(BaseUrl, headers=headers).content
