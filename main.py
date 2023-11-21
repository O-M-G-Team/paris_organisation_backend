from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from model import ParisDB, Result
from database import (
    fetch_one_sport_info,
    fetch_all_sport_infos,
    update_sport_result,
    fetch_api
)

# App object
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.get("/")
async def read_root():
    return {"paris": "organisation"}


@app.get("/api/data-ioc")
async def ioc_api():
    res = await fetch_api()
    return res


@app.get("/paris_org/olympic/sport_info")
async def get_sport_info():
    response = await fetch_all_sport_infos()
    return response


@app.get("/paris_org/olympic/{sport_id}", response_model=ParisDB)
async def get_sport_detail_by_sport_id(sport_id):
    response = await fetch_one_sport_info(sport_id)
    if response:
        return response
    raise HTTPException(404, f"There is no item with this sport_id {sport_id}")


@app.put("/paris_org/olympic/enter_result", response_model=Result)
async def put_sport_result(sport_request: Result):
    """Update the result of each sport id"""
    response = await update_sport_result(sport_request.sport_id, sport_request.result)
    if response == "forbidden countries":
        raise HTTPException(403, f"Counties are not allowed. They are not in participating country list.")
    if response:
        return response
    raise HTTPException(404, f"There is no sport_result item with this sport_id {sport_request.sport_id}")
