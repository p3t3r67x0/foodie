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


    @router.get('/', response_description='List all markets')
    async def list_markets(request: Request):
        latitude = 53.67515
        longitude = 10.22593
        distance = 4000

        query = {'loc': {'$nearSphere': {'$geometry': {'type': 'Point', 'coordinates': [latitude, longitude] }, '$maxDistance': distance}}}
        filter = {'_id': False}

        docs = request.app.db['markets'].find(query, filter).to_list(length=10000)

        markets = []

        for doc in await docs:
            id = {'id': doc['id']}
            wawi = {'wawi': doc['wawi']}
            markets.append({**doc['address'], **wawi, **id})

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
