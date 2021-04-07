#!/usr/bin/env python3

import json

from pymongo import MongoClient, GEOSPHERE, DESCENDING, ASCENDING


def connect_database():
    client = MongoClient('mongodb://localhost:27017/')
    db = client['discounter']

    return db


def insert_spatial_data(db, data):
    data['discounter'] = 'edeka'

    lat = float(data['coordinates']['lat'])
    lng = float(data['coordinates']['lng'])

    data['city'] = data['contact']['address']['city']['name']
    data['postalCode'] = data['contact']['address']['city']['postalCode']
    data['streetWithNumber'] = data['contact']['address']['streetWithNumber']
    data['state'] = data['contact']['address']['state']
    data['headline'] = data['name']

    del data['contact']
    del data['coordinates']

    if lat is None or lng is None:
        return

    geo_data = {'loc': {'type': 'Point', 'coordinates': [lat, lng]}}

    merged_data = {**data, **geo_data}

    try:
        db['markets'].insert(merged_data)
        print(merged_data)
    except Exception as e:
        print(e)


if __name__ == '__main__':
    db = connect_database()
    db['markets'].create_index([('id', ASCENDING), ('wawi', ASCENDING)], unique=True, partialFilterExpression={'id': {'$type': 'number'}, 'wawi': {'$type': 'string'}})
    db['markets'].create_index([('discounter', ASCENDING), ('streetWithNumber', ASCENDING)], unique=True)
    db['markets'].create_index([('loc', GEOSPHERE)])

    with open('edeka_markets_merged_sorted.json', 'r') as f:
        data = f.read()
        entries = json.loads(data)

        for entry in entries:
            insert_spatial_data(db, entry)
