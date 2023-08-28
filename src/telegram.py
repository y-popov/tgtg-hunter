import logging
import requests


class Telegram:
    markdown_escape = str.maketrans({
         '=': r'\=', '-': r'\-', '.': r'\.', '_': r'\_',
         '*': r'\*', '[': r'\[', ']': r'\]', '(': r'\(',
         ')': r'\)', '~': r'\~', '`': r'\`', '>': r'\>',
         '#': r'\#', '+': r'\+', '|': r'\|', '!': r'\!',
         '{': r'\{', '}': r'\}'
    })

    def __init__(self, token: str, default_chat: str):
        self.token = token
        self.chat_id = default_chat

    def send_message(self, message: str, chat_id: str = None):
        chat_id = chat_id or self.chat_id
        params = {'chat_id': chat_id,
                  'parse_mode': 'MarkdownV2',
                  'text': message}
        r = requests.get(f'https://api.telegram.org/bot{self.token}/sendMessage', params=params)
        if r.status_code != 200:
            logging.error(r.text)
