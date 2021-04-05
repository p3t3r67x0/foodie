#!/usr/bin/env python3


import requests
import cloudscraper

from lxml import html


def main():
    scraper = cloudscraper.create_scraper()

    url = 'https://www.lidl.de/de/filialsuche/s940'

    req = scraper.get(url)

    if req.status_code != 200:
        return

    res = req.text

    markup = html.fromstring(res)
    cities = markup.xpath("//dl[contains(@class, 'store-listing')]")

    for city in cities:
        markets = city.xpath('./dd')

        for market in markets:
            links = market.xpath('./a')

            for link in links:
                print(f'https://www.lidl.de{link.get("href")}')


if __name__ == '__main__':
    main()
