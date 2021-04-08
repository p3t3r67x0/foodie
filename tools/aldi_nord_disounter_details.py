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
    elements = markup.xpath("//div[@class='mod-stores__overview']/table/tbody/tr")

    for element in elements:
        rows = element.xpath('./td')

        tmp_adr = {}
        tmp_opn = {}

        for row in rows:
            address = row.xpath("./div[@class='mod-stores__overview-address']")
            openhours = row.xpath("./div[@class='mod-stores__overview-openhours']")

            if len(openhours) > 0:
                opening = []

                for openhour in openhours:
                    weekday = openhour.xpath("./span[@itemprop='openingHours']/text()")[0]
                    hours = openhour.xpath("./time[@itemprop='openingHours']/text()")[0]

                    opening.append(f'{weekday.strip()} {hours.strip()}')

                tmp_opn['openingHours'] = ' '.join(opening)

            if len(address) > 0:
                tmp_adr['discounter'] = 'aldi nord'
                tmp_adr['postalCode'] = address[0].xpath("./span[@itemprop='postalCode']/text()")[0]
                tmp_adr['streetWithNumber'] = address[0].xpath("./span[@itemprop='streetAddress']/text()")[0]
                tmp_adr['city'] = address[0].xpath("./span[@itemprop='addressLocality']/text()")[0]

        if bool(tmp_adr) and bool(tmp_opn):
            result = {**tmp_adr, **tmp_opn}

            with open('aldi_nord_discounter_details.json', 'a') as f:
                f.write(f'{result}\n')


if __name__ == '__main__':
    with open('aldi_nord_city_links.csv', 'r') as f:
        lines = f.readlines()

        for line in lines:
            extract_html(line.strip())
