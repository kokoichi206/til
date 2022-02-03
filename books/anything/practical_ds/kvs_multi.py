import gzip
import pickle
from pathlib import Path
from collections import namedtuple
from itertools import count
import requests
import random
from hashlib import sha224
from concurrent.futures import ProcessPoolExecutor

Path("db").mkdir(exist_ok=True)
Datum = namedtuple("Datum", ["depth", "domain", "html", "links"])


def get_diget(url):
    return sha224(bytes(url, "utf8")).hexdigest()[:24]

def flash(url, datum):
    # keyt となる url の hash 値を計算（長すぎるのをトリムする）
    key = get_diget(url)
    # value となる Datum 型のシリアライズと圧縮
    value = gzip.compress(pickle.dumps(datum))
    # db フォルダーに hash 値のファイル名で書き込む
    with open(f"db/{key}", "wb") as fp:
        fp.write(value)

def isExists(url):
    key = get_diget(url)
    if Path(f"db/{key}").exists():
        return True
    else:
        return False

def parallel(arg):
    url, depth = arg
    if isExists(uel):
        return
    depth = 1
    dummy_html = "<html>dummy</html>"
    dummy_domain = "example.com"
    dummy_links = ["1", "2", "3"]
    datum = Datum(depth=depth, domain=dummy_domain, html=dummy_html, links=dummy_links)
    flash(url, datum)

# ランダムな URL に対して実験を行う
dummy_urls = [f"{k:04d}" for k in range(1000)]
dummy_urls = [(random.choice(dummy_urls), i) for i in range(10000)]
with ProcessPoolExecutor(max_workers=8) as exe:
    exe.map(parallel, dummy_urls)
