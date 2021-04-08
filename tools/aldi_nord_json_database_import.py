#!/usr/bin/env python3

import json

from pymongo import MongoClient, GEOSPHERE, DESCENDING, ASCENDING


def connect_database():
    client = MongoClient('mongodb://localhost:27017/')
    db = client['discounter']

    return db


def insert_spatial_data(db, data):
    lat = float(data['lat'])
    lng = float(data['lng'])

    data['headline'] = ''
    data['district'] = ''
    data['state'] = ''

    del data['lat']
    del data['lng']

    if lat is None or lng is None:
        return

    geo_data = {'loc': {'type': 'Point', 'coordinates': [lat, lng]}}

    merged_data = {**data, **geo_data}

    try:
        db['markets'].insert_one(merged_data)
        print(merged_data)
    except Exception as e:
        print(e)


if __name__ == '__main__':
    db = connect_database()
    db['markets'].create_index([('id', ASCENDING), ('wawi', ASCENDING)], unique=True, partialFilterExpression={'id': {'$type': 'number'}, 'wawi': {'$type': 'string'}})
    db['markets'].create_index([('discounter', ASCENDING), ('streetWithNumber', ASCENDING)], unique=True)
    db['markets'].create_index([('loc', GEOSPHERE)])

    with open('aldi_nord_discounter_complete.json', 'r') as f:
        entries = json.loads(f.read())

        for entry in entries:
            insert_spatial_data(db, entry)
