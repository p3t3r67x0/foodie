from fastapi import APIRouter, Request, HTTPException
from OSMPythonTools.nominatim import Nominatim

nominatim = Nominatim()


def get_location_router(app):
    router = APIRouter()

    @router.get('/{query}', response_description='Get a forward location')
    async def show_location(query: str, request: Request):
        location = nominatim.query(query)
        data = location.toJSON()

        if len(data) > 0:
            return {
                'lat': data[0]['lat'],
                'lng': data[0]['lon']
            }

        raise HTTPException(status_code=404, detail='Location not found')

    return router
