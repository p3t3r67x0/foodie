#!/usr/bin/env python3

import re
import os
import json
import cloudscraper


def extract_location(data):
    scraper = cloudscraper.create_scraper()

    key = os.environ['KEY']
    street = data['streetWithNumber'].replace(' ', '+')
    query = f"{street}+{data['postalCode']}+{data['city']}+DE"
    params = f'?address={query}&key={key}'
    url = f'https://maps.googleapis.com/maps/api/geocode/json{params}'

    res = scraper.get(url)

    if res.status_code != 200:
        return

    response = json.loads(res.text)
    loc = response['results'][0]['geometry']['location']
    merge = {**data, **loc}

    with open('aldi_nord_discounter_complete.json', 'a') as f:
        f.write(f'{json.dumps(merge)}\n')
        print(merge)


if __name__ == '__main__':
    with open('aldi_nord_discounter_details.json', 'r') as f:
        lines = json.loads(f.read())

        for line in lines:
            extract_location(line)
