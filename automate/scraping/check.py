# テスト用データ
MOCK_PDF_INFOS = [
    {
        "title": "いたずら.pdf",
        "url": "https://nogizaka.com/itazura.saiko",
        "updated_at": "01/03",
        "tag": "かわいいの天才",
    },
    {
        "title": "乃木撮.pdf",
        "url": "https://nogizaka.com/nogisatsu.hogehoge",
        "updated_at": "01/03",
        "tag": "",
    },
    {
        "title": "日向撮.pdf",
        "url": "https://hinatazaka.com/hinatazaka.hogehoge",
        "updated_at": "01/03",
    },
    {
        "title": "さくら撮(仮).pdf",
        "url": "https://sakurazaka.com/sakurazaka.hogehoge",
        "updated_at": "01/03",
    },
    {
        "title": "光の角度.pdf",
        "url": "https://nogizaka.com/hikari",
        "updated_at": "01/03",
    },
]

import config
database_id = config.DATABASE_ID


def get_only_new_since(date, pdf_info):
    results = []
    for i in range(len(pdf_info)):
        try:
            print(pdf_info["ba"])
        except:
            print("Name doesn't exist")
    return results

# 自分のDBの設定に応じて変更させる
KEY_INFOS = [
    {
        "name": "title",    # Notionで定義した名前
        "property": "title",    # DBの形にあわさる
        "type": "text"
    },
    {
        "name": "url",
        "property": "url",    # DBの形にあわさる
        "type": None,
    },
    {
        "name": "tag",
        "property": "rich_text",
        "type": "text",
    },
]

def make_query_body(pdf_info):
    # 一番重要なproperties(中身)を作る
    properties = {}
    for i in range(len(KEY_INFOS)):
        key_info = KEY_INFOS[i]
        key_name = key_info["name"]
        try:
            if (key_info["type"]):
                this_type = [{key_info["type"]: {
                        # 名前を合わせる必要がある
                        "content": pdf_info[key_name],
                    }}]
            else:
                this_type = pdf_info[key_name]
            properties[key_name] = {
                key_info["property"]: this_type,
            }
        except KeyError:
            # pdf_infoがその情報を持ってない場合スキップ
            continue
    print(properties)

    # 生成したpropertiesを元に、リクエストボディを作る
    body = {
        "parent": {
            "database_id": database_id
        },
        "properties": properties
    }
    return body
    

if __name__ == "__main__":
    get_only_new_since("07/21", MOCK_PDF_INFOS)
    pdf_infos = MOCK_PDF_INFOS
    for pdf_info in pdf_infos:
        body = make_query_body(MOCK_PDF_INFOS[0])
        print(body)
        print("-----------------")
        import notion_api
        notion_api.post_field(body)
