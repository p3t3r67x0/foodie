#!/usr/bin/env python3


import requests
import cloudscraper

from lxml import html


def main():
    scraper = cloudscraper.create_scraper()

    url = 'https://www.rewe.de/marktseite/thueringen/'

    req = scraper.get(url)

    if req.status_code != 200:
        return

    res = req.text

    markup = html.fromstring(res)
    markets = markup.xpath("//div[@class='font-style-body four-columns']/p")

    for market in markets:
        links = market.xpath('./a')

        for link in links:
            print(f'- {link.get("href")}\n')


if __name__ == '__main__':
    main()
