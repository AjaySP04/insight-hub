# db/mongo_db.py
from typing import List, Optional
from fastapi import HTTPException
from motor.motor_asyncio import AsyncIOMotorClient

from app.configs import config
from app.logger.logger import logger

class MongoDB:
    _client = None

    @classmethod
    async def connect(cls):
        uri = cls.construct_mongo_uri()
        if cls._client is None:
            cls._client = AsyncIOMotorClient(uri)
    
    @classmethod
    async def close(cls):
        if cls._client is not None:
            cls._client.close()
            cls._client = None

    @staticmethod
    def construct_mongo_uri():
        if config.DATABASE_URL:
            return config.DATABASE_URL
        
        db_host = config.DATABASE_HOST
        db_port = config.DATABASE_PORT
        db_name = config.DATABASE_NAME
        db_user = config.DATABASE_USER
        db_password = config.DATABASE_PASSWORD

        auth_str = f"{db_user}:{db_password}@" if db_user and db_password else ""
        db_str = f"/{db_name}" if db_name else ""

        return f"mongodb://{auth_str}{db_host}:{db_port}{db_str}?authSource=admin"
    
    @classmethod
    def get_client(cls):
        if cls._client is None:
            raise HTTPException(status_code=500, detail="MongoDB not connected")
        return cls._client

    @classmethod
    def get_db(cls, db_name: str = ""):
        client = cls.get_client()
        if db_name == "":
            db_name = config.DATABASE_NAME
        return client.get_database(db_name)
    
    @classmethod
    async def count_documents(cls, collection_name: str, filter: dict):
        db = cls.get_db()
        collection = db.get_collection(collection_name)
        count = await collection.count_documents(filter)
        return count

    @classmethod
    async def find(cls, collection_name: str, filter: dict, limit: int = 10, skip: int = 0, sort: Optional[str] = None):
        db = cls.get_db()
        collection = db.get_collection(collection_name)

        cursor = collection.find(filter).skip(skip).limit(limit)
        if sort:
            cursor.sort(sort)

        documents = [document async for document in cursor]
        return documents
    
    @classmethod
    async def find_one(cls, collection_name: str, filter: dict):
        db = cls.get_db()
        collection = db.get_collection(collection_name)
        return await collection.find_one(filter)

    @classmethod
    async def insert_one(cls, collection_name: str, document: dict):
        db = cls.get_db()
        collection = db.get_collection(collection_name)
        result = await collection.insert_one(document)
        return result

    @classmethod
    async def update_one(cls, collection_name: str, filter: dict, update: dict):
        db = cls.get_db()
        collection = db.get_collection(collection_name)
        result = await collection.update_one(filter, {"$set": update})
        return result

    @classmethod
    async def delete_one(cls, collection_name: str, filter: dict):
        db = cls.get_db()
        collection = db.get_collection(collection_name)
        result = await collection.delete_one(filter)
        return result
