from pixivpy3 import AppPixivAPI
import time
import os


def download():
    api = AppPixivAPI()
    # not working now
    api.login("id", "password")
    result = api.search_illust(word="おっぱい")

    n = 0
    for i in range(200):
        if not hasattr(result, "illusts"): break

        cnt = 0
        for illust in result.illusts:
            if illust["total_bookmarks"] >= 5:
                lists = []
                if hasattr(illust, "meta_pages"):
                    for j, meta in enumerate(illust["meta_pages"]):
                        if ("img_urls" not in meta.keys() or
                            "large" not in meta["image_urls"]):
                            continue
                        else:
                            lists.append(meta["image_urls"]["large"])
                if hasattr(illust, "image_urls") and hasattr(illust["image_urls"], "large"):
                    lists.append(illust["image_urls"]["large"])
                lists = list(set(lists))

                if not os.path.exists("oppai_img_raw"):
                    os.mkdir("oppai_img_raw")
                for img in lists:
                    api.download(img, path="oppai_img_raw")
                    cnt += 1

        n += cnt

        print("i = ", i, "images = ", cnt, "total = ", n)

        result = api.search_illust(**api.parse_qs(result.next_url))
        time.sleep(5)

if __name__ == "__main__":
    download()
