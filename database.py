from model import ParisDB
import requests
from dateutil import parser
from decouple import config


# mongodb driver
import motor.motor_asyncio


if config('TEST', default=False, cast=bool):
    client = motor.motor_asyncio.AsyncIOMotorClient(config("TEST_DB", default='mongodb://localhost:27017'))
    database = client.ParisDB
    collection = database.test_sport_info
else:
    client = motor.motor_asyncio.AsyncIOMotorClient(config("ACTUAL_DB", default='mongodb://localhost:27017'))
    database = client.ParisDB
    collection = database.sport_info


# fetch from IOC and store in Paris database
async def fetch_api():

    try:
        res = requests.get(config('IOC_PATH'))
        res.raise_for_status()
        data = res.json()

        for event in data:
            sport_id = event["sport_id"]
            sport_name = event["sport_name"]
            sport_type = event["sport_type"]
            participating_country = event["participating_country"]
            date_time = parser.parse(event["datetime"])
            result = {}
            if "result" in event:
                result = event["result"]

            existing_sport_info = await collection.find_one({"sport_id": sport_id})

            if existing_sport_info:
                info = await fetch_one_sport_info(sport_id)
                if len(info['result']) != 0:
                    await update_sport_info(
                        sport_id, sport_name, participating_country, date_time, info[
                            'result'], sport_type
                    )
                else:
                    await update_sport_info(
                        sport_id, sport_name, participating_country, date_time, result, sport_type
                    )
            else:
                new_sport_info = {
                    "sport_id": sport_id,
                    "sport_name": sport_name,
                    "sport_type": sport_type,
                    "participating_country": participating_country,
                    "date_time": date_time,
                    "result": {}
                }

                await create_sport_info(new_sport_info)

        return "Sport info updated or created successfully"
    except requests.RequestException as e:
        return f"Failed to fetch data from the API: {str(e)}"


async def update_sport_result(sport_id, result):
    try:
        document = await collection.find_one({"sport_id": sport_id})
        participating_country = document["participating_country"]
        is_in_participating_country = True
        for key, value in result.items():
            for country in value:
                if country not in participating_country:
                    is_in_participating_country = False
                    break
        if not is_in_participating_country:
            return "forbidden countries"
        document = await collection.find_one_and_update({"sport_id": sport_id}, {'$set': {"result": result}})
        return document
    except:
        return False


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
