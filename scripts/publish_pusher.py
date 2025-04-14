import pusher
from os import environ


PUSHER_APP_ID = environ.get('PUSHER_APP_ID')
PUSHER_KEY = environ.get('PUSHER_KEY')
PUSHER_SECRET = environ.get('PUSHER_SECRET')
PUSHER_HOST = environ.get('PUSHER_HOST')

def publish():
    pusher_client = pusher.Pusher(
        app_id=PUSHER_APP_ID,
        key=PUSHER_KEY,
        secret=PUSHER_SECRET,
        host=PUSHER_HOST,
        ssl=True,
    )
    # Trigger an event
    channel_name = 'my-channel'
    event_name = 'my-event'
    data = {'message': 'Hello, World!'}
    pusher_client.trigger(channel_name, event_name, data)


if __name__ == '__main__':
    publish()



