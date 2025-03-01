# This script interacts with the Slack API to download images from a specified Slack channel.
# It uses the Slack SDK to authenticate and fetch messages from the channel.
# The script identifies image files in the messages and downloads them using the requests library.
# The Slack API token is loaded from an environment variable for secure access.

import os
import requests
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from dotenv import load_dotenv

# Initialize a Web API client
load_dotenv()
slack_token = os.environ["SLACK_BOT_TOKEN"]
client = WebClient(token=slack_token)

def download_image(file_url, file_name):
    try:
        # Use the requests library to download the file
        headers = {"Authorization": f"Bearer {slack_token}"}
        response = requests.get(file_url, headers=headers)
        
        if response.status_code == 200:
            with open(file_name, 'wb') as f:
                f.write(response.content)
            print(f"Image downloaded: {file_name}")
        else:
            print(f"Failed to download image. Status code: {response.status_code}")
    except SlackApiError as e:
        print(f"Error downloading image: {e.response['error']}")


def get_images_from_channel(channel_id):
    try:
        response = client.conversations_history(channel=channel_id)
        if response['ok']:
            for message in response['messages']:
                if 'files' in message:
                    for file in message['files']:
                        if file['mimetype'].startswith('image/'):
                            download_image(file['url_private'], file['name'])
    except SlackApiError as e:
        print(f"Error fetching channel history: {e.response['error']}")

# Example usage
channel_id = "C08FKSBS4S1"
get_images_from_channel(channel_id)
