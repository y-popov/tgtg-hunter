import os
import json
import flask
import functions_framework
from tgtg import TgtgClient


from src.telegram import Telegram
from src.tg_tg import compose_message

tg_bot_token = os.getenv('TG_BOT_TOKEN')
tg_chat = os.getenv('TG_CHAT')
email = os.getenv('EMAIL')
credentials_string = os.getenv('TGTG_CREDENTIALS')
track_list = ['513666', '910441']


def main():
    tg = Telegram(token=tg_bot_token, default_chat=tg_chat)

    credentials = json.loads(credentials_string)
    client = TgtgClient(**credentials)
    records = client.get_items(favorites_only=True, with_stock_only=True)

    for record in records:
        if record['item']['item_id'] in track_list:
            message = compose_message(record)
            tg.send_message(message)


@functions_framework.http
def handler(request: flask.Request):
    main()
    return 'ok'


if __name__ == '__main__':
    main()
