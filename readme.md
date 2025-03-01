Data →
Find easy, medium, hard images of whiteboard
Create custom images of whiteboard

Slack →
Create slackbot
Observe channel for image upload
Trigger an event (langflow)

OpenAI →
Enter Excalidraw schema
Create system prompt to process incoming image
Test out on playground to ensure it matches excalidraw expectation
Upload JSON to excalidraw to verify

Langflow + AstraDB →
Receive image from slack
Embed and store images
Pipe it to OpenAI and get structured output .excalidraw
Share it back on slack to user via slackbot

View →
Final image in excalidraw

setup
`pip install slack_sdk requests openai unstructured cassandra-driver python-dotenv pillow`
