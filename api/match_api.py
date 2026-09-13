from fastapi import APIRouter, HTTPException
import json
from pathlib import Path

router = APIRouter(prefix="/matches", tags=["Match Calendar"])

DATA_FILE = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "matches.json"
)


def load_match_data():
    with open(DATA_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


@router.get("/")
def get_all_matches():
    """
    Return the synthetic match calendar.
    """
    return load_match_data()


@router.get("/{date}")
def get_match_by_date(date: str):
    """
    Return match information for a specific date.
    """

    data = load_match_data()

    for match in data:
        if match["date"] == date:
            return match

    raise HTTPException(
        status_code=404,
        detail=f"No match found for {date}"
    )