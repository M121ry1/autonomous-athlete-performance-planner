from datetime import datetime, timedelta

from engine.readiness_engine import analyze_readiness


def generate_session(readiness_status, days_to_match, availability):
    """
    Generate a training session based on the current
    performance analysis.

    This is a synthetic performance-planning system.
    It is not a medical or injury-management system.
    """

    # Limited availability always receives a lower-load session.
    if availability == "limited":

        return {
            "session_type": "Recovery / Low-load",
            "intensity": "low",
            "duration_min": 35,
            "target_load": "low",
            "objective": "Support recovery and maintain routine"
        }

    # Very close to competition.
    if days_to_match is not None and days_to_match <= 1:

        return {
            "session_type": "Pre-competition activation",
            "intensity": "low",
            "duration_min": 30,
            "target_load": "low",
            "objective": "Prepare for upcoming competition"
        }

    # 2-3 days before competition.
    if days_to_match is not None and days_to_match <= 3:

        if readiness_status == "high":

            return {
                "session_type": "Competition preparation",
                "intensity": "moderate",
                "duration_min": 60,
                "target_load": "moderate",
                "objective": "Develop competition-specific readiness"
            }

        return {
            "session_type": "Tactical preparation",
            "intensity": "low-moderate",
            "duration_min": 45,
            "target_load": "low-moderate",
            "objective": "Prepare tactically while controlling workload"
        }

    # Normal training when readiness is high.
    if readiness_status == "high":

        return {
            "session_type": "Development session",
            "intensity": "high",
            "duration_min": 75,
            "target_load": "high",
            "objective": "Develop performance capacity"
        }

    # Moderate readiness.
    if readiness_status == "moderate":

        return {
            "session_type": "Controlled development",
            "intensity": "moderate",
            "duration_min": 60,
            "target_load": "moderate",
            "objective": "Maintain development with controlled workload"
        }

    # Reduced readiness.
    return {
        "session_type": "Recovery-focused session",
        "intensity": "low",
        "duration_min": 40,
        "target_load": "low",
        "objective": "Reduce planned workload while maintaining activity"
    }


def generate_training_plan(start_date, end_date):
    """
    Generate an autonomous daily training plan.

    The planner obtains performance analysis for each
    available date and creates a training recommendation.
    """

    start = datetime.strptime(
        start_date,
        "%Y-%m-%d"
    )

    end = datetime.strptime(
        end_date,
        "%Y-%m-%d"
    )

    plan = []

    current_date = start

    while current_date <= end:

        date_string = current_date.strftime("%Y-%m-%d")

        analysis = analyze_readiness(date_string)

        if analysis is not None:

            readiness_status = analysis["readiness_status"]

            availability = analysis["wellness"]["availability"]

            days_to_match = analysis["days_to_next_match"]

            session = generate_session(
                readiness_status,
                days_to_match,
                availability
            )

            plan.append({
                "date": date_string,
                "readiness_score": analysis["readiness_score"],
                "readiness_status": readiness_status,
                "availability": availability,
                "days_to_next_match": days_to_match,
                "session": session
            })

        current_date += timedelta(days=1)

    return plan