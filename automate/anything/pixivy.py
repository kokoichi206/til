# ランキングの3位までの画像をdownloadするサンプル
import time
from pixivpy3 import *

api = AppPixivAPI()
# aapi.login("ここにユーザ名","ここにパスワード") ## 使えなくなった
api.auth(refresh_token="1_LQSxRIkcgxYrMW2DFqm0zUHRE7rvBMg-1kGAkeMBg")
json_result = api.illust_ranking()
for illust in json_result.illusts[:3]:
    api.download(illust.image_urls.large)
    time.sleep(1)
