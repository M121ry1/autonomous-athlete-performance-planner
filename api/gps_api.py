from fastapi import APIRouter, HTTPException
import json
from pathlib import Path

router = APIRouter(prefix="/gps", tags=["GPS / Workload"])

DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "gps_data.json"


def load_gps_data():
    with open(DATA_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


@router.get("/")
def get_all_gps_data():
    """
    Return all synthetic GPS/workload records.
    """
    return load_gps_data()


@router.get("/{date}")
def get_gps_by_date(date: str):
    """
    Return GPS/workload data for a specific date.
    """

    data = load_gps_data()

    for record in data:
        if record["date"] == date:
            return record

    raise HTTPException(
        status_code=404,
        detail=f"No GPS data found for {date}"
    )