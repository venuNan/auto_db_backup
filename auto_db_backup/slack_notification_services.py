from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

# Your Slack bot token
slack_token = "xoxb-your-slack-bot-token"

# Initialize the WebClient
client = WebClient(token=slack_token)

# Channel or user ID where you want to send the message
channel_id = "C1234567890"  # Replace with the actual channel or user ID

# Message content
message = "Hello from Python!"

try:
    response = client.chat_postMessage(
        channel=channel_id,
        text=message
    )
    print(f"Message sent: {response['ts']}")
    
except SlackApiError as e:
    print(f"Error sending message: {e.response['error']}")
