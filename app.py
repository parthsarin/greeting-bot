"""
File: app.py
------------

The main flask app for the greeting bot.
"""
from flask import Flask, request
import requests
from os import environ

app = Flask(__name__)
MESSAGE_FILE = 'message.txt'
SLACK_API_TOKEN = environ.get('SLACK_API_TOKEN')
SLACK_HEADERS = {
    'Authorization': f'Bearer {SLACK_API_TOKEN}'
}


def handle_welcome(user_id: str):
    """
    Performs the Slackbot response when the user should be welcomed:
    1. Opens a direct message with the user.
    2. Sends the welcome message in the MESSAGE_FILE.
    """
    channel_req = requests.post(
        "https://slack.com/api/conversations.open",
        headers=SLACK_HEADERS,
        json={
            'users': [user_id]
        }
    )

    if not channel_req.ok and (data := channel_req.json()).get('ok', False):
        # Something went wrong
        return
    
    channel_id = data.get('channel', {}).get('id')

    # Post the message
    msg = open(MESSAGE_FILE, 'r').read()
    requests.post(
        "https://slack.com/api/chat.postMessage",
        headers=SLACK_HEADERS, 
        json={
            'channel': channel_id,
            'text': msg
        }
    )


@app.route("/", methods=['POST'])
def index():
    payload = request.json

    # Slackbot challenge
    if "challenge" in payload:
        return payload['challenge']

    user_id = payload['event']['user']
    handle_welcome(user_id)

    return {'success': True}