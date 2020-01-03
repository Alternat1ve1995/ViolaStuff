import os
import json
import requests
from time import sleep

PROCESSED = []


def get_random_idea():
    response = requests.get('https://drawingpractice.ru/generator-idey/')
    content_str = response.content.decode(response.encoding)
    key1 = content_str.find('id="story">') + len('id="story">')
    result = content_str[content_str.find('id="story">') + len('id="story">'):content_str.find('</div>', key1)]
    result = result.strip(" \t\n")
    return result


def load_config():
    with open('%s/tgBot/secrets.json' % os.path.realpath('.')) as file:
        file_data = file.read()
        return json.loads(file_data)


def send_response(updates, token):
    message = updates['result'][-1]['message']
    if message['text'] == 'idea' and message['message_id'] not in PROCESSED:
        requests.post("https://api.telegram.org/bot%s/sendMessage" % token['token'], data={
            'chat_id': message['chat']['id'],
            'text': get_random_idea()
        })
    PROCESSED.append(message['message_id'])


def main():
    while True:
        token = load_config()
        res = requests.get("https://api.telegram.org/bot%s/getUpdates" % token['token'])
        con_str = json.loads(res.content.decode("utf-8"))
        send_response(con_str, token)
        sleep(5)


main()

# getUpdates
# sendMessage
# https://api.telegram.org/bot'%s'%load_config/getUpdates
# https://api.telegram.org/bot<token>/METHOD_NAME
