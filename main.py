import requests
import os
from dotenv import load_dotenv
from urllib.parse import urlparse
import argparse


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('link')
    return parser


def shorten_link(token, url):
    response = requests.get(url)
    response.raise_for_status()
    method_url='https://api.vk.ru/method/utils.getShortLink'
    payload={
        'access_token' : token,
        'v' : '5.199',
        'url' : url
    }
    response = requests.get(method_url,params=payload)
    response.raise_for_status()
    short_url = response.json()['response']['short_url']
    return short_url


def count_clicks(token, url):
    response = requests.get(url)
    response.raise_for_status()
    parsed = urlparse(url)
    method_url = 'https://api.vk.ru/method/utils.getLinkStats'
    payload = {
        'access_token' : token,
        'v' : '5.199',
        'key' : parsed.path[1:],
        'interval' : 'forever'

    }
    response = requests.get(method_url, params=payload)
    response.raise_for_status()
    if response.json()['response']['stats'] == []:
        return '0'
    else:
        return response.json()['response']['stats'][0]['views']


def is_shorten_link(url):
    parsed = urlparse(url)
    vk_netloc = 'vk.cc'
    flag_shorten_link = vk_netloc != parsed.netloc
    return flag_shorten_link


if __name__ == '__main__':
    load_dotenv()
    token = os.environ['VK_TOKEN']
    parser = create_parser()
    parsed_link = parser.parse_args()
    url = parsed_link.link
    if is_shorten_link(url):
        try:
            short_url = shorten_link(token, url)
        except requests.exceptions.HTTPError:
            short_url='Неправильная ссылка'
        print(short_url)
    else:
        try:
            count_clicks = count_clicks(token, url)
        except requests.exceptions.HTTPError:
            count_clicks='Неправильная ссылка'
        print(count_clicks)




