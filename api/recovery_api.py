from fastapi import APIRouter, HTTPException
import json
from pathlib import Path

router = APIRouter(prefix="/recovery", tags=["Recovery"])

DATA_FILE = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "recovery_data.json"
)


def load_recovery_data():
    with open(DATA_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


@router.get("/")
def get_all_recovery_data():
    """
    Return all synthetic recovery records.
    """
    return load_recovery_data()


@router.get("/{date}")
def get_recovery_by_date(date: str):
    """
    Return recovery information for a specific date.
    """

    data = load_recovery_data()

    for record in data:
        if record["date"] == date:
            return record

    raise HTTPException(
        status_code=404,
        detail=f"No recovery data found for {date}"
    )