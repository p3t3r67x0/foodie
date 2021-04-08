#!/usr/bin/env python3


import requests
import cloudscraper

from lxml import html


def main():
    scraper = cloudscraper.create_scraper()

    url = 'https://www.aldi-nord.de/tools/filialen-und-oeffnungszeiten.html'

    req = scraper.get(url)

    if req.status_code != 200:
        return

    res = req.text

    markup = html.fromstring(res)
    counties = markup.xpath("//div[@class='mod-stores__multicolumn']/p")

    for county in counties:
        link = county.xpath('./a')
        print(f'https://www.aldi-nord.de{link[0].get("href")}')


if __name__ == '__main__':
    main()
