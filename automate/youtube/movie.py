#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import pickle
from apiclient.discovery import build

import config


API_KEY = config.API_KEY
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'
SEARCH_TEXT = '筒井あやめ'

youtube = build(
    YOUTUBE_API_SERVICE_NAME,
    YOUTUBE_API_VERSION,
    developerKey=API_KEY
)

response = youtube.search().list(q=SEARCH_TEXT, part='id,snippet', maxResults=25).execute()
# print(response)

dict_list = []
for item in response.get('items', []):
    
    if item['id']['kind'] != 'youtube#video':
        continue
    new_dict = {}
#    print(json.dumps(item, indent=2, ensure_ascii=False))
    # print(item['snippet']['channelId'])
    # print(item['id']['videoId'])
    # print(item['snippet']['title'])
    new_dict['title'] = item['snippet']['title']
    new_dict['videoId'] = item['id']['videoId']
    new_dict['channelId'] = item['snippet']['channelId']
    dict_list.append(new_dict)
#    print('*' * 10)

f = open('list_searchId.txt', 'wb')
pickle.dump(dict_list,f)

for dic in dict_list:
    CHANNEL_ID = dic['channelId']
    video_id = dic['videoId']
    response = youtube.videos().list(
      part = 'snippet,statistics',
      id = video_id
      ).execute()

    for item in response.get("items", []):
        if item["kind"] != "youtube#video":
            continue
        print('*' * 10)
        print(json.dumps(item, indent=2, ensure_ascii=False))
        print('*' * 10)

g = open('search_result.txt','wb')
pickle.dump(response,g)
