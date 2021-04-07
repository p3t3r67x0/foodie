#!/usr/bin/env python3

import json

from pymongo import MongoClient, GEOSPHERE, DESCENDING, ASCENDING


def connect_database():
    client = MongoClient('mongodb://localhost:27017/')
    db = client['discounter']

    return db


def insert_spatial_data(db, data):
    data['discounter'] = 'penny'

    lat = float(data['latitude'])
    lng = float(data['longitude'])

    data['openingHours'] = data['openingSentence']
    data['streetWithNumber'] = f"{data['street']} {data['houseNumber']}"
    data['headline'] = data['marketName']
    data['district'] = ''
    data['state'] = ''

    del data['latitude']
    del data['longitude']
    del data['marketName']
    del data['closesAtFriday']
    del data['closesAtMonday']
    del data['closesAtSaturday']
    del data['closesAtSunday']
    del data['closesAtThursday']
    del data['closesAtTuesday']
    del data['closesAtWednesday']
    del data['opensAtFriday']
    del data['opensAtMonday']
    del data['opensAtSaturday']
    del data['opensAtSunday']
    del data['opensAtThursday']
    del data['opensAtTuesday']
    del data['opensAtWednesday']
    del data['openingSentence']

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

    with open('penny_markets_cleaned.json', 'r') as f:
        data = f.read()
        entries = json.loads(data)

        for entry in entries:
            insert_spatial_data(db, entry)
