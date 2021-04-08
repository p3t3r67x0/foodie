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
    elements = markup.xpath("//div[@class='mod-stores__multicolumn']/p")

    for element in elements:
        link = element.xpath('./a')

        with open('aldi_nord_discounter_details.csv', 'a') as f:
            f.write(f'https://www.aldi-nord.de{link[0].get("href")}\n')


if __name__ == '__main__':
    with open('aldi_nord_counties_links.csv', 'r') as f:
        lines = f.readlines()

        for line in lines:
            extract_html(line.strip())
