import requests
from pprint import pprint
import json

import config

def get_request_url(end_point):
    return f'https://api.notion.com/v1/{end_point}'

def get_db_check():
    notion_api_key = config.API_SECRET
    databases_id = config.DATABASE_ID
    headers = {"Authorization": f"Bearer {notion_api_key}",
            "Content-Type": "application/json",
            "Notion-Version": "2021-05-13"}

    response = requests.request('GET', url=get_request_url(f'databases/{databases_id}'), headers=headers)

    pprint(response.json())


def make_post_body(key, value):
    KEY_NAME = "Name"
    VALUE_NAME = "なまえだよ"
    key = key
    value = value
    body = {
        "parent": {
            "database_id": databases_id},
        "properties": {
            KEY_NAME: {"title": [
                {"text": {"content": key}}
                ]
            },
            VALUE_NAME: {
                "rich_text": [
                {"text": {"content": value}}
                ]
            }
        }}

def post_field(key, value):
    response = requests.request('POST', url=get_request_url('pages'), headers=headers, data=json.dumps(make_post_body(key, value)))
    pprint(response.json())

if __name__ == "__main__":
    get_db_check()

    # 投稿のチェック
    key = "post test"
    value = "from python"
    post_field(key, value)
