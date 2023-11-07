import os

from dotenv import load_dotenv
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

load_dotenv()

app = App(
    token=os.environ["SLACK_BOT_TOKEN"],
    # signing_secret=os.environ["SLACK_SIGNING_SECRET"],
)

@app.event("app_mention")
def handle_mention(event, say):
    user = event["user"]
    thread_ts = event["ts"]
    say(
        thread_ts=thread_ts,
        text=f"Hi there, <@{user}>!",
    )


if __name__ == "__main__":
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()
