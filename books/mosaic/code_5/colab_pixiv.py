## pixiv.jsonをランタイムにコピー
!cp gdrive/My\ Drive/colab\ data/pixiv.json pixiv.json

# Bounding Box のデータをダウンロードする
!git clone https://github.com/koshian2/OpyDataset
!mv OpyDataset/bbox.zip bbox.zip
!cp bbox.zip gdrive/My\ Drive/colab\ data/bbox.zip
!unzip bbox.zip > /dev/null


# =============================================

from pixivpy3 import AppPixivAPI, PixivAPI
import time
import json
import os
import glob
from tqdm import tqdm
from PIL import Image
import imagehash

# ログイン制限があるのでローカルPCでやる必要がある
def download_images(output_dir="images"):
    jsons = sorted(glob.glob("bbox/*"))
    # mapperを作る
    mapper = {}
    for f in jsons:
        filename = os.path.basename(f).replace(".json", "")
        artwork_id = int(filename.split("_")[0])
        with open(f) as fp:
            ahash = json.load(fp)["dataset"]["average_hash"]
        if artwork_id not in mapper.keys():
            mapper[artwork_id] = [[filename, ahash]]
        else:
            mapper[artwork_id].append([filename, ahash])

    # pixivのID,パスを読み込む
    with open("pixiv.json") as fp:
        pixiv = json.load(fp)

    api = AppPixivAPI()
    # api.login(pixiv["pixiv_id"], pixiv["password"])
    api.auth(refresh_token=pixiv["refresh_token"])
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

    for i, (artwork_id, target_images) in tqdm(enumerate(mapper.items())):
        # セッション切れ対策に一定期間に再度ログインする
        if i % 1000 == 999:
            #api.login(pixiv["pixiv_id"], pixiv["password"])
            api.auth(refresh_token=pixiv["refresh_token"])
            print("Account re-login")

        try:
            json_result = api.illust_detail(artwork_id)
        except Exception as ex:
            print(ex)
            print("last count : ", i ,"last artwork id : ",artwork_id)
            continue

        urls = []
        # 作品が消えている可能性がある
        if ("illust" not in json_result.keys() or
            "image_urls" not in json_result["illust"].keys() or
            "large" not in json_result["illust"]["image_urls"].keys()):
            print(id, json_result)
            continue
        else:
            urls = [json_result["illust"]["image_urls"]["large"]]
        
        if "meta_pages" in json_result["illust"].keys():
            for page in json_result["illust"]["meta_pages"]:
                if ("image_urls" in page.keys() and
                    "large" in page["image_urls"]):
                    urls.append(page["image_urls"]["large"])

        urls = sorted(list(set(urls)))
        download_urls = [] # url + hash
        for a in urls:
            for bf, bh in target_images:
                if os.path.basename(a).replace(".jpg", "") == bf:
                    download_urls.append([a, bh])

        for url, original_hash in download_urls:
            api.download(url, path=output_dir)
            # API limit対策、負荷対策
            time.sleep(1)
            local_path = output_dir + "/" + os.path.basename(url)
            target_hash = imagehash.average_hash(Image.open(local_path))
            if original_hash != str(target_hash):
                os.remove(local_path)
                print("File removed because of hash mismatched")

if __name__ == "__main__":
    download_images()



