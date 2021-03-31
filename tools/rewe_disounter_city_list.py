#!/usr/bin/env python3


import json
import requests
import cloudscraper

from lxml import html


def extract_json(city):
    print(f'extracting rewe city ${city}')

    scraper = cloudscraper.create_scraper()

    url = 'https://www.rewe.de/market/content/marketsearch/'

    data = {
        'searchString': '',
        'city': f'{city}',
        'pageSize': '500',
        'page': '0'
    }

    req = scraper.post(url, data=data)

    if req.status_code != 200:
        return

    markets = json.loads(req.text)

    for market in markets['markets']:
        print(market)

        with open('rewe_discounter_details.json', 'a') as f:
            f.write(json.dumps(market))



if __name__ == '__main__':
    with open('rewe_city_names.csv', 'r') as f:
        lines = f.readlines()

        for line in lines:
            extract_json(line.strip())
