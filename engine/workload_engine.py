import json
from pathlib import Path
from statistics import mean


DATA_FILE = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "gps_data.json"
)


def load_gps_data():
    """Load synthetic GPS/workload data."""
    with open(DATA_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def calculate_acute_load(records, window=3):
    """
    Calculate recent workload using the last `window` sessions.
    """
    if not records:
        return 0

    recent_records = records[-window:]

    return round(
        sum(record["training_load"] for record in recent_records),
        2
    )


def calculate_chronic_baseline(records):
    """
    Calculate the historical average workload.

    This is a project-specific baseline using the available
    synthetic historical records.
    """
    if not records:
        return 0

    loads = [
        record["training_load"]
        for record in records
    ]

    return round(mean(loads), 2)


def calculate_workload_ratio(acute_load, chronic_baseline):
    """
    Calculate a project-specific workload planning index.

    This should not be interpreted as a clinical or medical metric.
    """

    if chronic_baseline == 0:
        return 0

    return round(
        acute_load / chronic_baseline,
        2
    )


def analyze_workload(target_date=None):
    """
    Produce workload analysis for the available synthetic data.
    """

    records = load_gps_data()

    if target_date:
        records = [
            record
            for record in records
            if record["date"] <= target_date
        ]

    if not records:
        return {
            "acute_load": 0,
            "chronic_baseline": 0,
            "workload_ratio": 0,
            "recent_sessions": 0
        }

    acute_load = calculate_acute_load(records)

    chronic_baseline = calculate_chronic_baseline(records)

    workload_ratio = calculate_workload_ratio(
        acute_load,
        chronic_baseline
    )

    return {
        "acute_load": acute_load,
        "chronic_baseline": chronic_baseline,
        "workload_ratio": workload_ratio,
        "recent_sessions": min(3, len(records))
    }