#!/usr/bin/env python3


import json

from pymongo import MongoClient, GEOSPHERE, DESCENDING, ASCENDING


def connect_database():
    client = MongoClient('mongodb://localhost:27017/')
    db = client['discounter']

    return db


def insert_spatial_data(db, data):
    print(data)

    lat = data['coordinates']['lat']
    lng = data['coordinates']['lng']

    del data['coordinates']

    if lat is None or lng is None:
        geo_data = {}
    else:
        geo_data = {'loc': {'type': 'Point', 'coordinates': [lat, lng]}}

    merged_data = {**data, **geo_data}

    try:
        db['markets'].insert(merged_data)
    except Exception as e:
        print(e)


if __name__ == '__main__':
    db = connect_database()
    db['markets'].create_index([('id', ASCENDING)], unique=True)
    db['markets'].create_index([('id', ASCENDING), ('wawi', ASCENDING)], unique=True)
    db['markets'].create_index([('loc', GEOSPHERE)])

    with open('lidl_discounter_details.json', 'r') as f:
        data = f.read()
        entries = json.loads(data)

        for entry in entries:
            insert_spatial_data(db, entry)
