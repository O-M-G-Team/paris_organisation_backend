from typing import AsyncIterator
import pytest
from httpx import AsyncClient
from main import app
import pytest_asyncio
import asyncio
from decouple import config


if not config('TEST', default=False, cast=bool):
    pytest.skip("Skipping tests because Test configuration is set to False", allow_module_level=True)


@pytest_asyncio.fixture
async def client() -> AsyncIterator[AsyncClient]:
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client

@pytest.fixture(scope='session')
def event_loop():
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()

   
pytestmark = pytest.mark.asyncio


async def test_read_root(client: AsyncClient) -> None:
    """Get the root api."""
    response = await client.get("/")
    assert response.status_code == 200
    assert response.json() == {"paris": "organisation"}

async def test_fetch_api(client: AsyncClient) -> None:
    """Get the sport information from ioc."""
    response = await client.get("/api/data-ioc")
    assert response.status_code == 200
    assert response.json() == "Sport info updated or created successfully"

async def test_get_sport_info(client: AsyncClient) -> None:
    """Get all sport information from poc database."""
    response = await client.get("/paris_org/olympic/sport_info")
    assert response.status_code == 200
    assert len(response.json()) != 0

async def test_get_sport_detail_by_valid_sport_id(client: AsyncClient) -> None:
    """Get sport detail by sport_id using valid sport_id."""
    response = await client.get("/paris_org/olympic/ATH0102")
    json_response = response.json()
    assert response.status_code == 200
    assert json_response["sport_name"] == "Women's 20km Race Walk"
    assert json_response["sport_type"] == "Athletics"
    assert json_response["participating_country"] == [] #TODO add participating_country
    assert json_response["date_time"] == "2024-08-01T07:30:00"

async def test_get_sport_detail_by_invalid_sport_id(client: AsyncClient) -> None:
    """Get sport detail by sport_id using invalid sport_id."""
    response = await client.get("/paris_org/olympic/invalid_sport_id")
    assert response.status_code == 404
    assert response.json()["detail"] == "There is no item with this sport_id invalid_sport_id"


async def test_put_sport_result_with_valid_sport_id_and_result_format(client: AsyncClient) -> None:
    """Update sport result to the existing sport datail with the given sport_id."""
    payload = {"sport_id": "ATH0102", "result": {"gold": ["UK"], "silver": ['Japan'], "bronze": ["China"]}}
    response = await client.put("/paris_org/olympic/enter_result", json=payload)
    assert response.status_code == 200

async def test_put_sport_result_with_invalid_sport_id(client: AsyncClient) -> None:
    """Update sport result to the existing sport datail with the invalid sport_id."""
    payload = {"sport_id": "wrong_id", "result": {"gold": ["UK"], "silver": ['Japan'], "bronze": ["China"]}}
    response = await client.put("/paris_org/olympic/enter_result", json=payload)
    assert response.status_code == 404

async def test_put_sport_result_with_wrong_result_format(client: AsyncClient) -> None:
    """
    Update sport result to the existing sport datail with the wrong result format 
    using normal string instead of list as a value.
    """
    payload = {"sport_id": "wrong_id", "result": {"gold": "USA", "silver": 'Japan', "bronze": "China"}}
    response = await client.put("/paris_org/olympic/enter_result", json=payload)
    assert response.status_code == 422
