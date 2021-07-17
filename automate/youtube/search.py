#!/usr/bin/python

from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser

import config


# Set DEVELOPER_KEY to the API key value from the APIs & auth > Registered apps
# tab of
#   https://cloud.google.com/console
# Please ensure that you have enabled the YouTube Data API for your project.
DEVELOPER_KEY = config.API_KEY
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

def youtube_saerch_video(options):
  youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
    developerKey=DEVELOPER_KEY)

  videos_response = youtube.videos().list(
    part="id,snippet,statistics",
    id=options.id
  ).execute()

  videos = []

  for result in videos_response.get("items", []):
    videos.append("(%s) [%s] <%6s> %s" % (result["id"],
                                          result["snippet"]["channelId"],
                                          result["statistics"]["viewCount"],
                                          result["snippet"]["title"]))
  print("\n".join(videos), "\n")

if __name__ == "__main__":
  argparser.add_argument("--id", help="VideoIDs", default="Sq5QW3YqipM")
  args = argparser.parse_args()

  try:
    youtube_saerch_video(args)
  except HttpError as e:
    print("An HTTP error %d occurred:\n%s" % (e.resp.status, e.content))
