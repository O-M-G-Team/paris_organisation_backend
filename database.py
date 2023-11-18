from model import ParisDB
import requests
from datetime import datetime
from dateutil import parser

# mongodb driver
import motor.motor_asyncio

client = motor.motor_asyncio.AsyncIOMotorClient('mongodb://localhost:27017')

database = client.ParisDB

collection = database.sport_info

# fetch from IOC and store in Paris database

async def fetch_api():

    try:
        res = requests.get("https://nongnop.azurewebsites.net/match_table/Final")
        res.raise_for_status()
        data = res.json()

        for event in data:
            sport_id = event["sport_id"]
            sport_name = event["sport_name"]
            sport_type = event["sport_type"]
            participating_country = event["participating_country"]
            date_time = parser.parse(event["datetime"])
            result = {}

            existing_sport_info = await collection.find_one({"sport_id": sport_id})

            if existing_sport_info:
                await update_sport_info(
                    sport_id, sport_name, participating_country, date_time, sport_type
                )
            else:
                new_sport_info = {
                    "sport_id": sport_id,
                    "sport_name": sport_name,
                    "sport_type": sport_type,
                    "participating_country": participating_country,
                    "date_time": date_time, 
                    "result": result
                }

                doc = await create_sport_info(new_sport_info)

        return "Sport info updated or created successfully"
    except requests.RequestException as e:
        return f"Failed to fetch data from the API: {str(e)}"



###################### Example CRUD request######################
async def update_sport_result(sport_id, result):
    document = await collection.find_one_and_update({"sport_id": sport_id},{'$set': {"result": result}})
    return document


async def fetch_one_sport_info(sport_id):
    document = await collection.find_one({"sport_id": sport_id})
    return document


async def fetch_all_sport_infos():
    sport_infos = []
    cursor = collection.find({})
    async for document in cursor:
        sport_infos.append(ParisDB(**document))
    return sport_infos


async def create_sport_info(sport_info):
    document = sport_info
    # find existing sport_id
    try:
        temp = await collection.find_one({"sport_id": sport_info["sport_id"]})
        if temp["sport_id"] == sport_info["sport_id"]:
            return False
    except:
        result = await collection.insert_one(document)
        return document


async def update_sport_info(sport_id, sport_name, participating_country, date_time, result, sport_type):

    await collection.update_one({"sport_id": sport_id}, {"$set": {
        "sport_id": sport_id,
        "sport_name": sport_name,
        "sport_type": sport_type,
        "participating_country": participating_country,
        "date_time": date_time,
        "result": result
    }})
    document = await collection.find_one({"sport_id": sport_id})
    return document


async def remove_sport_info(sport_id):
    await collection.delete_one({"sport_id": sport_id})
    return True

##################################################################
