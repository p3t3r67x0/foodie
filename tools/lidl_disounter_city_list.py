#!/usr/bin/env python3

import re
import json
import requests
import cloudscraper

from lxml import html


def extract_html(url):
    scraper = cloudscraper.create_scraper()

    res = scraper.get(url)

    if res.status_code != 200:
        return

    markup = html.fromstring(res.text)
    element = markup.xpath("//script[@type='text/javascript']")[11]

    js = element.xpath('./text()')[0]
    markets = re.findall(r'eval\((.*)\)', js.strip())

    for market in json.loads(markets[0]):
        del market['url']
        del market['bake']
        del market['filename']
        del market['hotdrinks']
        del market['directory']
        del market['information']
        del market['package']
        del market['OH']
        del market['AR']
        del market['NF']
        del market['X']
        del market['Y']
        del market['LABEL1']
        del market['LABEL2']
        del market['COUNTRY']
        del market['CITY']
        del market['ZIPCODE']
        del market['VT']
        del market['HOUSENUMBER']
        del market['CITYDISTRICT']

        coordinates = json.loads(market['geoInformation'].replace('X', '"lat"').replace('Y', '"lng"'))

        market['coordinates'] = {}
        market['coordinates']['lat'] = float(coordinates['lat'].replace(',', '.'))
        market['coordinates']['lng'] = float(coordinates['lng'].replace(',', '.'))

        del market['geoInformation']

        print(market)

        with open('lidl_discounter_details.json', 'a') as f:
            f.write(f'{json.dumps(market)},\n')


if __name__ == '__main__':
    with open('lidl_city_links.csv', 'r') as f:
        lines = f.readlines()

        for line in lines:
            extract_html(line.strip())
