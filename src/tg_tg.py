import json
from tgtg import TgtgClient
from datetime import datetime


def parse_tgtg_time(time_string):
    return datetime.strptime(time_string, '%Y-%m-%dT%H:%M:%S%z')


def get_credentials(email, outfile='credentials.json'):
    client = TgtgClient(email=email)
    credentials = client.get_credentials()
    with open(outfile, 'w') as f:
        json.dump(credentials, f, indent=2)


def compose_message(record: dict):
    start = parse_tgtg_time(record['pickup_interval']['start'])
    end = parse_tgtg_time(record['pickup_interval']['end'])
    message = f"{record['items_available']} {record['item_type']}(s) of {record['item']['name']} available " \
              f"in {record['store']['store_name']}! From {start.hour}:{start.minute} to {end.hour}:{end.minute}"
    return message
