import httpx

from fastapi import APIRouter, Request, HTTPException
from config import settings


async def request_httpx(url):
    async with httpx.AsyncClient() as client:
        return await client.get(url)


def get_location_router(app):
    router = APIRouter()

    @router.get('/{query}', response_description='Get an osm suggestion')
    async def osm_suggestions(query: str, request: Request):
        res = await request_httpx(f'{settings.PHOTON_URL}/api?q={query}&limit=15')

        if res.status_code != 200:
            raise HTTPException(status_code=404, detail='No suggestions found')

        data = []

        if 'features' in res.json():
            for r in res.json()['features']:
                forbidden = ['park', 'water', 'service', 'industrial']

                if 'osm_value' in r['properties'] and r['properties']['osm_value'] in forbidden:
                    continue

                d = {}

                if 'street' in r['properties']:
                    d['street'] = r['properties']['street']
                elif 'name' in r['properties']:
                    d['street'] = r['properties']['name']
                else:
                    d['street'] = ''

                if 'housenumber' in r['properties']:
                    d['housenumber'] = r['properties']['housenumber']
                else:
                    d['housenumber'] = ''

                if 'postcode' in r['properties']:
                    d['postcode'] = r['properties']['postcode']
                else:
                    d['postcode'] = ''

                if 'city' in r['properties']:
                    d['city'] = r['properties']['city']
                else:
                    d['city'] = ''

                if d['street'] and d['postcode'] or d['street'] and d['city']:
                    s = ' '.join([v for k, v in d.items()])
                    x = s.replace('  ', ' ').strip()

                    if x not in data:
                        data.append(x)

        return data

    return router
