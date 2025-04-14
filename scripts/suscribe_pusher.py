import json
from os import environ

import websocket

PUSHER_KEY = environ.get('PUSHER_KEY')
PUSHER_HOST = environ.get('PUSHER_HOST')

CHANNEL_NAME = "test-academy"
EVENT_NAME = "WhatsappSession.RefreshSessions"

ws_url = f"wss://{PUSHER_HOST}/app/{PUSHER_KEY}"

print(f"Connecting to {ws_url}...")

def on_message(ws, message):
    """Callback when a message is received."""
    data = json.loads(message)
    event = data.get("event")

    # Handle events
    if event == "pusher:connection_established":
        print("Connected to Pusher!")
        # Subscribe to a channel
        payload = {
            "event": "pusher:subscribe",
            "data": {
                "channel": CHANNEL_NAME
            }
        }
        ws.send(json.dumps(payload))
    elif event == EVENT_NAME:
        print(f"Received event {EVENT_NAME}: {data.get('data')}")


def on_error(ws, error):
    """Callback when an error occurs."""
    print(f"Error: {error}")


def on_close(ws, close_status_code, close_msg):
    """Callback when the connection is closed."""
    print("Closed connection.")


def on_open(ws):
    """Callback when the connection is opened."""
    print("Connection opened.")


# Create the WebSocket connection
ws = websocket.WebSocketApp(
    ws_url,
    on_message=on_message,
    on_error=on_error,
    on_close=on_close,
)
ws.on_open = on_open

# Start the WebSocket connection
ws.run_forever()
