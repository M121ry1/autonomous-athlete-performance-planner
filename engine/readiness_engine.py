import json
from pathlib import Path

from engine.workload_engine import analyze_workload
from engine.recovery_engine import analyze_recovery


MATCH_FILE = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "matches.json"
)

WELLNESS_FILE = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "wellness_data.json"
)


def load_matches():

    with open(MATCH_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def load_wellness():

    with open(WELLNESS_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def get_wellness(date):

    records = load_wellness()

    for record in records:
        if record["date"] == date:
            return record

    return None


def get_next_match(date):

    matches = load_matches()

    future_matches = [
        match
        for match in matches
        if match["date"] > date
    ]

    if not future_matches:
        return None

    future_matches.sort(
        key=lambda x: x["date"]
    )

    return future_matches[0]


def calculate_days_to_match(current_date, match_date):

    from datetime import datetime

    current = datetime.strptime(
        current_date,
        "%Y-%m-%d"
    )

    match = datetime.strptime(
        match_date,
        "%Y-%m-%d"
    )

    return (match - current).days


def determine_readiness(
    recovery_score,
    fatigue_indicator,
    workload_ratio,
    availability,
    days_to_match
):
    """
    Calculate a project-specific synthetic readiness score.

    Score range:
        0 - 100

    Higher score = greater planning readiness.

    This is a synthetic research/planning metric and is
    not a medical or clinical assessment.
    """

    score = 100

    # -------------------------------------------------
    # 1. Recovery contribution
    # -------------------------------------------------

    if recovery_score < 70:
        recovery_penalty = (70 - recovery_score) * 0.7
        score -= recovery_penalty

    # -------------------------------------------------
    # 2. Fatigue contribution
    # -------------------------------------------------

    if fatigue_indicator > 50:

        score -= 15

    elif fatigue_indicator > 35:

        score -= 8

    # -------------------------------------------------
    # 3. Workload contribution
    # -------------------------------------------------

    if workload_ratio > 1.5:

        score -= 15

    elif workload_ratio > 1.2:

        score -= 8

    elif workload_ratio > 1.0:

        score -= 4

    # -------------------------------------------------
    # 4. Availability contribution
    # -------------------------------------------------

    if availability == "limited":

        score -= 10

    # -------------------------------------------------
    # 5. Competition proximity
    # -------------------------------------------------

    if days_to_match is not None:

        if days_to_match <= 1:

            score -= 5

        elif days_to_match <= 3:

            score -= 2

    # -------------------------------------------------
    # Keep score between 0 and 100
    # -------------------------------------------------

    score = max(
        0,
        min(100, round(score))
    )

    # -------------------------------------------------
    # Readiness classification
    # -------------------------------------------------

    if score >= 75:

        status = "high"

    elif score >= 55:

        status = "moderate"

    else:

        status = "reduced"

    return score, status


def recommend_training(
    readiness_status,
    days_to_match,
    availability
):

    if availability == "limited":
        return {
            "training_type": "recovery / low-load session",
            "intensity": "low",
            "target_load": "low"
        }

    if days_to_match is not None:

        if days_to_match <= 1:
            return {
                "training_type": "pre-competition activation",
                "intensity": "low",
                "target_load": "low"
            }

        if days_to_match <= 3:

            if readiness_status == "high":
                return {
                    "training_type": "competition preparation",
                    "intensity": "moderate",
                    "target_load": "moderate"
                }

            return {
                "training_type": "tactical preparation",
                "intensity": "low-moderate",
                "target_load": "low-moderate"
            }

    if readiness_status == "high":

        return {
            "training_type": "development session",
            "intensity": "high",
            "target_load": "high"
        }

    if readiness_status == "moderate":

        return {
            "training_type": "controlled development session",
            "intensity": "moderate",
            "target_load": "moderate"
        }

    return {
        "training_type": "recovery-focused session",
        "intensity": "low",
        "target_load": "low"
    }


def analyze_readiness(date):

    workload = analyze_workload(date)

    recovery = analyze_recovery(date)

    wellness = get_wellness(date)

    next_match = get_next_match(date)

    if recovery is None or wellness is None:
        return None

    if next_match:

        days_to_match = calculate_days_to_match(
            date,
            next_match["date"]
        )

    else:
        days_to_match = None

    readiness_score, readiness_status = determine_readiness(
        recovery_score=recovery["recovery_score"],
        fatigue_indicator=recovery["fatigue_indicator"],
        workload_ratio=workload["workload_ratio"],
        availability=wellness["availability"],
        days_to_match=days_to_match
    )

    recommendation = recommend_training(
        readiness_status,
        days_to_match,
        wellness["availability"]
    )

    return {
        "date": date,

        "workload": workload,

        "recovery": recovery,

        "wellness": {
            "mood": wellness["mood"],
            "energy": wellness["energy"],
            "stress": wellness["stress"],
            "motivation": wellness["motivation"],
            "availability": wellness["availability"]
        },

        "next_match": next_match,

        "days_to_next_match": days_to_match,

        "readiness_score": readiness_score,

        "readiness_status": readiness_status,

        "training_recommendation": recommendation
    }