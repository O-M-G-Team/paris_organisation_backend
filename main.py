from database import (
    fetch_one_sport_info,
    fetch_all_sport_infos,
    create_sport_info,
    update_sport_info,
    remove_sport_info, 
    fetch_api
)
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from model import ParisDB, Result
from typing import List, Dict
from datetime import datetime

# App object
app = FastAPI()

from database import (
    fetch_one_sport_info,
    fetch_all_sport_infos,
    create_sport_info,
    update_sport_info,
    remove_sport_info,
    update_sport_result,
    fetch_api
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:5173'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.get("/")
def read_root():
    return {"paris": "organisation"}

###################### Example CRUD request######################

@app.put("/paris_org/olympic/enter_result", response_model=Result)
async def put_sport_result(sport_request: Result):
    """Update the result of each sport id"""
    response = await update_sport_result(sport_request.sport_id, sport_request.result)
    if response:
        return response
    raise HTTPException(404, f"there is no sport_result item with this sport_id {sport_request.sport_id}")


@app.get("/paris_org/olympic/sport_info")
async def get_sport_info():
    response = await fetch_all_sport_infos()
    return response

@app.get("/api/data-ioc")
async def ioc_api():
    res = await fetch_api()
    return res


@app.get("/api/sport_info/{sport_id}", response_model=ParisDB)
async def get_sport_info_by_sport_id(sport_id):
    response = await fetch_one_sport_info(sport_id)
    if response:
        return response
    raise HTTPException(
        404, f"there is no sport_info item with this sport_id {sport_id}")


@app.post("/api/sport_info", response_model=ParisDB)
async def post_sport_info(sport_info: ParisDB):
    response = await create_sport_info(sport_info.model_dump())
    if response:
        return response
    raise HTTPException(404, f"The sport_id has already been used.")


@app.put("/api/sport_info/{sport_id}", response_model=ParisDB)
async def put_sport_info(sport_id: str, sport_name: str,  participating_country: List[str], date_time: datetime, result: List[Dict]):
    response = await update_sport_info(sport_id, sport_name, participating_country, date_time, result)
    if response:
        return response
    raise HTTPException(
        404, f"there is no sport_info item with this sport_id {sport_id}")


@app.delete("/api/sport_info/{sport_id}")
async def delete_sport_info(sport_id):
    response = await remove_sport_info(sport_id)
    if response:
        return "Succesfully deleted sport_info item"
    raise HTTPException(
        404, f"there is no sport_info item with this sport_id {sport_id}")


@app.get("/paris_org/olympic/{sport_id}", response_model=ParisDB)
async def get_sport_detail_by_sport_id(sport_id):
    response = await fetch_one_sport_info(sport_id)
    if response:
        return response
    raise HTTPException(404, f"There is no item with this sport_id {sport_id}")
