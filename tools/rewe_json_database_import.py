#!/usr/bin/env python3

import json

from pymongo import MongoClient, GEOSPHERE, DESCENDING, ASCENDING


def connect_database():
    client = MongoClient('mongodb://localhost:27017/')
    db = client['discounter']

    return db


def insert_spatial_data(db, data):
    for key, value in data['address'].items():
        data[key] = value

    data['id'] = data['id']
    data['wawi'] = data['wawi']
    data['openingHours'] = data['openingHours']['condensed']
    data['discounter'] = 'rewe'

    lat = data['geoLocation']['latitude']
    lng = data['geoLocation']['longitude']

    del data['type']
    del data['phone']
    del data['marketManager']
    del data['regionShort']
    del data['closedFrom']
    del data['temporaryClosedFrom']
    del data['closedUntil']
    del data['temporaryClosedUntil']
    del data['firstOpeningDate']
    del data['openOnSunday']
    del data['dortmund']
    del data['nahkauf']
    del data['specialOpening']
    del data['opened']
    del data['temporaryClosed']
    del data['state']
    del data['advertisingCounty']
    del data['company']
    del data['holiday']
    del data['holidayDate']
    del data['specialOpeningHours']
    del data['stateShort']
    del data['externalLink']
    del data['pickupMarket']
    del data['specialStart']
    del data['specialEnd']
    del data['openedUntil']
    del data['geoLocation']
    del data['address']

    if lat is None or lng is None:
        return

    geo_data = {'loc': {'type': 'Point', 'coordinates': [lat, lng]}}

    merged_data = {**data, **geo_data}

    try:
        db['markets'].insert(merged_data)
    except Exception as e:
        print(e)


if __name__ == '__main__':
    db = connect_database()
    db['markets'].create_index([('id', ASCENDING), ('wawi', ASCENDING)], unique=True, partialFilterExpression={'id': {'$type': 'number'}, 'wawi': {'$type': 'string'}})
    db['markets'].create_index([('discounter', ASCENDING), ('streetWithNumber', ASCENDING)], unique=True)
    db['markets'].create_index([('loc', GEOSPHERE)])

    with open('rewe_discounter_details.json', 'r') as f:
        data = f.read()
        entries = json.loads(data)

        for entry in entries:
            insert_spatial_data(db, entry)
