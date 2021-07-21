import time
from selenium import webdriver
from bs4 import BeautifulSoup

import config

DRIVER_PATH = config.DRIVER_PATH
# Webページを取得して解析する
DEFAULT_URL = "https://drive.google.com/drive/folders/12CQH0j9-MHLMDUL-Ku-BV15lqy_SlVrn"

def get_pdf_names(url=DEFAULT_URL, doesUseBrowser=False):
    #ヘッドレスモードでブラウザを起動
    options = webdriver.ChromeOptions()
    if not doesUseBrowser:
        options.add_argument('--headless')

    driver = webdriver.Chrome(DRIVER_PATH, options=options)

    driver.get(url)

    # リスト表示に切り替えるためのボタンをクリックする
    btn_to_list = driver.find_element_by_xpath('//div[@data-tooltip="リスト表示"]')
    print(btn_to_list)
    btn_to_list.click()

    #
    # FIXME
    # 待つ時間を、DOMレンダリング完了後、までに変更する
    time.sleep(15)
    print('get HTML start')
    html = driver.page_source.encode('utf-8')
    soup = BeautifulSoup(html, "html.parser")

    BASE_URL = "https://drive.google.com/file/d/"
    SUFFIX = "/view?usp=sharing"

    # 
    # FIXME
    # もっといいやり方ありそう...
    # divだけにしておくと、その子要素のspanが取れない
    divspans = soup.findAll(["div", "span"])

    for i in range(len(divspans)):
        div = divspans[i]
        if div.has_attr("data-id"):
            id = div["data-id"]
            pdf_url = BASE_URL + id + SUFFIX
            print(pdf_url)
            
            inner_divs = div.findChildren("div" , recursive=True)

            for i in range(len(inner_divs)):
                inner_div = inner_divs[i]
                if inner_div.text[-4:] == '.pdf':
                    print(inner_div.text)
                    break

            TRY_NUM = 120
            for j in range(i, i+TRY_NUM):
                inner_span = divspans[j]
                if inner_span.has_attr("data-tooltip"):
                    span_text = inner_span["data-tooltip"]
                    if span_text[:4] == "最終更新":
                        split_date = span_text.split(":")
                        if len(split_date) == 2:
                            # "最終更新 : 07/03" みたいな場合
                            updated_at = split_date[1].strip()
                        elif len(split_date) == 3:
                            # "最終更新 : 20:03" みたいな場合
                            updated_at = ':'.join(split_date[1:])
                        else:
                            continue
                        print(updated_at)
                        break

    driver.close()

if __name__ == "__main__":
    get_pdf_names(url=DEFAULT_URL, doesUseBrowser=False)
    