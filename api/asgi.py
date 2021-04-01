#!/usr/bin/env python3

import uvicorn

from fastapi import FastAPI
from fastapi_users import FastAPIUsers
from fastapi_users.db import MongoDBUserDatabase
from motor.motor_asyncio import AsyncIOMotorClient
from config import settings

from apps.user.auth import jwt_authentication
from apps.user.models import User, UserCreate, UserUpdate, UserDB
from apps.user.routers import get_users_router
from apps.market.routers import get_market_router

app = FastAPI()


@app.on_event('startup')
async def configure_db_and_routes():
    app.mongodb_client = AsyncIOMotorClient(
        settings.DB_URL, uuidRepresentation='standard'
    )

    app.db = app.mongodb_client.get_default_database()

    user_db = MongoDBUserDatabase(UserDB, app.db['users'])

    app.fastapi_users = FastAPIUsers(
        user_db,
        [jwt_authentication],
        User,
        UserCreate,
        UserUpdate,
        UserDB,
    )

    app.include_router(get_users_router(app))
    app.include_router(get_market_router(app))


@app.on_event('shutdown')
async def shutdown_db_client():
    app.mongodb_client.close()


if __name__ == '__main__':
    uvicorn.run(
        'asgi:app',
        host=settings.HOST,
        reload=settings.DEBUG_MODE,
        port=settings.PORT,
    )
