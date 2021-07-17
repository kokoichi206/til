#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json

from apiclient.discovery import build

import config


API_KEY = config.API_KEY
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'
SEARCH_TEXT = '筒井あやめ'
# SEARCH_TEXT = 'ayaya'

youtube = build(
    YOUTUBE_API_SERVICE_NAME,
    YOUTUBE_API_VERSION,
    developerKey=API_KEY
)

response = youtube.search().list(q=SEARCH_TEXT, part='id,snippet', maxResults=25).execute()
print(response)
# print(type(response))
for item in response.get('items', []):
    if item['id']['kind'] != 'youtube#channels':
        continue
#    print('*' * 10)
    print(json.dumps(item, indent=2, ensure_ascii=False))
#    print('*' * 10)
