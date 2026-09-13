from fastapi import APIRouter, HTTPException
import json
from pathlib import Path

router = APIRouter(prefix="/wellness", tags=["Wellness"])

DATA_FILE = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "wellness_data.json"
)


def load_wellness_data():
    with open(DATA_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


@router.get("/")
def get_all_wellness_data():
    """
    Return all synthetic wellness records.
    """
    return load_wellness_data()


@router.get("/{date}")
def get_wellness_by_date(date: str):
    """
    Return wellness and availability information.
    """

    data = load_wellness_data()

    for record in data:
        if record["date"] == date:
            return record

    raise HTTPException(
        status_code=404,
        detail=f"No wellness data found for {date}"
    )