import requests
from bs4 import BeautifulSoup

# Webページを取得して解析する
# url = "https://drive.google.com/drive/folders/12CQH0j9-MHLMDUL-Ku-BV15lqy_SlVrn"
url = "https://drive.google.com/drive/folders/12CQH0j9-MHLMDUL-Ku-BV15lqy_SlVrn"
html = requests.get(url)
soup = BeautifulSoup(html.content, "html.parser")

BASE_URL = "https://drive.google.com/file/d/"
SUFFIX = "/view?usp=sharing"

# FIXME
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

        TRY_NUM = 30
        for j in range(i, i+TRY_NUM):
            print(j)
            inner_span = divspans[j]
            if inner_span.has_attr("data-tooltip"):
                span_text = inner_span["data-tooltip"]
                print(span_text)
                if span_text[-4:] == "最終更新":
                    split_date = span_text.split(":")
                    if len(split_date == 2):
                        # "最終更新 : 07/03" みたいな場合
                        updated_at = split_date[1].strip
                    else:
                        # "最終更新 : 20:03" みたいな場合
                        updated_at = ':'.join(split_date[1:])
                    print(updated_at)
                    break

      
        # test = div.findChildren("div", recursive=True)
        # print(test)
        # print(type(test))


    #   // pdfの名前の取得
    #   for (let i = 0; i < inner_divs.length; i++) {
    #     const inner_div = inner_divs[i];
    #     if (isPdfName(inner_div.innerHTML)){
    #       info["name"] = inner_div.textContent;
    #       pdfInfos.push(info);
    #       break
    #     }
    #   }

# for i in range(len(spans)):
#     span = spans[i]
#     print(span.text)

print(type(soup))
print(type(divspans[0]))
print(type(divspans[0].contents))

# import inspect
# for x in inspect.getmembers(divs[0], inspect.ismethod):
#   print(x[0])
#