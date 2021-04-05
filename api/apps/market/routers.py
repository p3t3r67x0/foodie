import re

from fastapi import APIRouter, Body, Request, HTTPException, status, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from .models import MarketModel, UpdateMarketModel


def get_market_router(app):
    router = APIRouter()

    @router.get('/{id}', response_description='Get a single market')
    async def show_market(id: str, request: Request):
        if (market := await request.app.db['markets'].find_one({'_id': id})) is not None:
            return market

        raise HTTPException(status_code=404, detail=f'Market {id} not found')


    @router.get('/{lat}/{lng}', response_description='List near markets')
    async def list_markets(lat: float, lng: float, request: Request):
        distance = 4000

        query = {'loc': {'$nearSphere': {'$geometry': {'type': 'Point', 'coordinates': [lat, lng] }, '$maxDistance': distance}}}
        filter = {'_id': False}

        docs = request.app.db['markets'].find(query, filter).to_list(length=9)

        markets = []

        for doc in await docs:
            print(doc)

            id = {'id': doc['id']}

            discounter = {'discounter': doc['discounter']}

            if 'wawi' in doc:
                wawi = {'wawi': doc['wawi']}
            else:
                wawi = {'wawi': ''}

            if 'headline' in doc:
                headline = {'headline': doc['headline']}
            else:
                headline = {'headline': ''}

            if isinstance(doc['address'], dict):
                address = doc['address']
            else:
                street_pattern = r'^[^\s][a-zA-Zäöü]+(?:[\s]{1})(?:[a-zA-Zäöü\.]+)'
                city_pattern = r'[a-zA-Zäöü]+(?:[\s]{1})(?:[a-zA-Zäöü\.]+)$'

                street = re.findall(street_pattern, doc['address'])
                house_number = re.findall(r'([\d-]+),', doc['address'])
                postal_code = re.findall(r'([\d]{5})', doc['address'])
                city = re.findall(city_pattern, doc['address'])

                address = {
                    'city': city[0],
                    'street': street[0],
                    'postalCode': postal_code[0],
                    'streetWithNumber': f'{street[0]} {house_number[0]}',
                    'houseNumber': house_number[0]
                }

                del doc['address']
                del doc['street']
                del doc['city']

            coordinates = {'coordinates': doc['loc']['coordinates']}

            markets.append({**address, **discounter, **headline, **coordinates, **wawi, **id})

        return markets


    @router.post('/', response_description='Add new market')
    async def create_market(request: Request, market: MarketModel = Body(...)):
        market = jsonable_encoder(market)
        new_market = await request.app.db['markets'].insert_one(market)

        created_market = await request.app.db['markets'].find_one(
            {'_id': new_market.inserted_id}
        )

        return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_market)


    @router.put('/{id}', response_description='Update a market')
    async def update_market(id: str, request: Request, market: UpdateMarketModel = Body(...)):
        market = {k: v for k, v in market.dict().items() if v is not None}

        if len(market) >= 1:
            update_result = await request.app.db['markets'].update_one(
                {'_id': id}, {'$set': market}
            )

            if update_result.modified_count == 1:
                if (
                    updated_market := await request.app.db['markets'].find_one({'_id': id})
                ) is not None:
                    return updated_market

        if (
            existing_market := await request.app.db['markets'].find_one({'_id': id})
        ) is not None:
            return existing_market

        raise HTTPException(status_code=404, detail=f'Market {id} not found')


    @router.delete('/{id}', response_description='Delete Market')
    async def delete_task(id: str, request: Request):
        delete_result = await request.app.db['tasks'].delete_one({'_id': id})

        if delete_result.deleted_count == 1:
            return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)

        raise HTTPException(status_code=404, detail=f'Market {id} not found')


    return router
