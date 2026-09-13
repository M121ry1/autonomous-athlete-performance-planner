from datetime import datetime, timedelta

from engine.readiness_engine import (
    determine_readiness,
    recommend_training
)

from planner.constraint_checker import (
    check_plan_constraints
)


def calculate_days_to_match(
    current_date,
    match_date
):

    current = datetime.strptime(
        current_date,
        "%Y-%m-%d"
    )

    match = datetime.strptime(
        match_date,
        "%Y-%m-%d"
    )

    return (match - current).days


def build_session(
    date,
    readiness_score,
    readiness_status,
    recovery_score,
    fatigue_indicator,
    availability,
    match_date
):

    days_to_match = calculate_days_to_match(
        date,
        match_date
    )

    # Match day
    if days_to_match == 0:

        return {
            "date": date,
            "readiness_score": readiness_score,
            "readiness_status": readiness_status,
            "availability": availability,
            "days_to_next_match": 0,
            "is_match_day": True,
            "session": {
                "session_type": "MATCH",
                "intensity": "competition",
                "duration_min": 90,
                "target_load": "competition",
                "objective": "Competition against scheduled opponent"
            }
        }

    recommendation = recommend_training(
        readiness_status,
        days_to_match,
        availability
    )

    return {
        "date": date,
        "readiness_score": readiness_score,
        "readiness_status": readiness_status,
        "availability": availability,
        "days_to_next_match": days_to_match,
        "is_match_day": False,
        "session": recommendation
    }


def generate_revised_plan(
    start_date,
    end_date,
    recovery_score,
    fatigue_indicator,
    workload_ratio,
    availability,
    match_date
):

    start = datetime.strptime(
        start_date,
        "%Y-%m-%d"
    )

    end = datetime.strptime(
        end_date,
        "%Y-%m-%d"
    )

    # Use a fixed project-specific workload index
    # representing the observed recent workload state.

    readiness_score, readiness_status = determine_readiness(
        recovery_score=recovery_score,
        fatigue_indicator=fatigue_indicator,
        workload_ratio=workload_ratio,
        availability=availability,
        days_to_match=calculate_days_to_match(
            start_date,
            match_date
        )
    )

    plan = []

    current = start

    while current <= end:

        date = current.strftime("%Y-%m-%d")

        days_to_match = calculate_days_to_match(
            date,
            match_date
        )

        daily_score, daily_status = determine_readiness(
            recovery_score=recovery_score,
            fatigue_indicator=fatigue_indicator,
            workload_ratio=workload_ratio,
            availability=availability,
            days_to_match=days_to_match
        )

        day_plan = build_session(
            date=date,
            readiness_score=daily_score,
            readiness_status=daily_status,
            recovery_score=recovery_score,
            fatigue_indicator=fatigue_indicator,
            availability=availability,
            match_date=match_date
        )

        plan.append(day_plan)

        current += timedelta(days=1)

    constraints = check_plan_constraints(
        plan
    )

    return {
        "plan_start": start_date,
        "plan_end": end_date,
        "match_date": match_date,
        "readiness_score": readiness_score,
        "readiness_status": readiness_status,
        "plan": plan,
        "constraint_check": constraints
    }


def create_replanning_demo():

    # ==================================================
    # INITIAL PLAN
    # ==================================================
    #
    # Baseline state:
    # Recovery is good, fatigue is relatively low,
    # workload is controlled, and availability is full.
    #

    initial_plan = generate_revised_plan(
        start_date="2026-09-12",
        end_date="2026-09-15",

        recovery_score=72,
        fatigue_indicator=30,
        workload_ratio=1.10,

        availability="full",

        match_date="2026-09-15"
    )

    # ==================================================
    # REVISION 1
    # ==================================================
    #
    # Athlete state becomes less favorable:
    # - Recovery decreases
    # - Fatigue increases
    # - Workload ratio increases
    # - Availability becomes limited
    #

    revision_1 = generate_revised_plan(
        start_date="2026-09-12",
        end_date="2026-09-15",

        recovery_score=52,
        fatigue_indicator=52,
        workload_ratio=1.80,

        availability="limited",

        match_date="2026-09-15"
    )

    # ==================================================
    # REVISION 2
    # ==================================================
    #
    # State changes again:
    # - Recovery improves
    # - Fatigue decreases
    # - Workload becomes more controlled
    # - Match moves from Sep 15 to Sep 14
    #

    revision_2 = generate_revised_plan(
        start_date="2026-09-12",
        end_date="2026-09-15",

        recovery_score=65,
        fatigue_indicator=38,
        workload_ratio=1.30,

        availability="full",

        match_date="2026-09-14"
    )

    # ==================================================
    # RETURN COMPLETE REPLANNING DEMONSTRATION
    # ==================================================

    return {
        "initial_plan": initial_plan,
        "revision_1": revision_1,
        "revision_2": revision_2
    }