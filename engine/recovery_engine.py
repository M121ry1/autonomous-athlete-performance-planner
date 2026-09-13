import json
from pathlib import Path


DATA_FILE = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "recovery_data.json"
)


def load_recovery_data():
    """Load synthetic recovery data."""

    with open(DATA_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def get_recovery_record(date):
    """Get recovery information for a specific date."""

    records = load_recovery_data()

    for record in records:
        if record["date"] == date:
            return record

    return None


def classify_recovery(recovery_score):
    """
    Convert recovery score into a simple project status.
    """

    if recovery_score >= 75:
        return "good"

    if recovery_score >= 60:
        return "moderate"

    return "reduced"


def calculate_fatigue_indicator(record):
    """
    Calculate a synthetic fatigue indicator.

    Higher value = greater planning concern.

    This is a project-specific indicator and is not
    a medical assessment.
    """

    recovery_score = record["recovery_score"]
    soreness = record["muscle_soreness"]
    stress = record["stress"]

    fatigue = (
        (100 - recovery_score) * 0.50
        + soreness * 0.25
        + stress * 0.25
    )

    return round(fatigue, 2)


def analyze_recovery(date):

    record = get_recovery_record(date)

    if record is None:
        return None

    recovery_score = record["recovery_score"]

    recovery_status = classify_recovery(
        recovery_score
    )

    fatigue_indicator = calculate_fatigue_indicator(
        record
    )

    return {
        "date": date,
        "recovery_score": recovery_score,
        "sleep_hours": record["sleep_hours"],
        "energy": record["energy"],
        "muscle_soreness": record["muscle_soreness"],
        "stress": record["stress"],
        "recovery_status": recovery_status,
        "fatigue_indicator": fatigue_indicator
    }