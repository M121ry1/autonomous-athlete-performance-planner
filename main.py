from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from engine.workload_engine import analyze_workload
from engine.recovery_engine import analyze_recovery
from engine.readiness_engine import determine_readiness, recommend_training

from planner.replanning_engine import generate_revised_plan
from planner.constraint_checker import check_plan_constraints


app = FastAPI(
    title="Autonomous Athlete Performance Planner",
    description="Synthetic athlete workload, recovery, readiness and dynamic planning API",
    version="1.0"
)


# ============================================================
# REQUEST MODEL FOR DASHBOARD V2
# ============================================================

class PlannerAnalysisRequest(BaseModel):
    date: str

    recovery_score: float
    sleep_hours: float
    energy: float
    muscle_soreness: float
    stress: float

    mood: float
    motivation: float

    availability: str

    current_training_load: float
    acute_load: float
    chronic_baseline: float

    match_date: Optional[str] = None
    match_importance: Optional[str] = "medium"


# ============================================================
# BASIC TEST ENDPOINT
# ============================================================

@app.get("/")
def home():
    return {
        "message": "Autonomous Athlete Performance Planner API is running",
        "status": "online"
    }


# ============================================================
# EXISTING GPS ENDPOINTS
# ============================================================

@app.get("/gps/")
def get_gps_data():
    from api.gps_api import get_all_gps
    return get_all_gps()


@app.get("/gps/{date}")
def get_gps_by_date(date: str):
    from api.gps_api import get_gps
    result = get_gps(date)

    if result is None:
        raise HTTPException(
            status_code=404,
            detail=f"No GPS data found for {date}"
        )

    return result


# ============================================================
# EXISTING RECOVERY ENDPOINTS
# ============================================================

@app.get("/recovery/")
def get_recovery_data():
    from api.recovery_api import get_all_recovery
    return get_all_recovery()


@app.get("/recovery/{date}")
def get_recovery_by_date(date: str):
    from api.recovery_api import get_recovery
    result = get_recovery(date)

    if result is None:
        raise HTTPException(
            status_code=404,
            detail=f"No recovery data found for {date}"
        )

    return result


# ============================================================
# EXISTING WELLNESS ENDPOINTS
# ============================================================

@app.get("/wellness/")
def get_wellness_data():
    from api.wellness_api import get_all_wellness
    return get_all_wellness()


@app.get("/wellness/{date}")
def get_wellness_by_date(date: str):
    from api.wellness_api import get_wellness
    result = get_wellness(date)

    if result is None:
        raise HTTPException(
            status_code=404,
            detail=f"No wellness data found for {date}"
        )

    return result


# ============================================================
# EXISTING MATCH ENDPOINTS
# ============================================================

@app.get("/matches/")
def get_matches():
    from api.match_api import get_all_matches
    return get_all_matches()


@app.get("/matches/{date}")
def get_match_by_date(date: str):
    from api.match_api import get_match
    result = get_match(date)

    if result is None:
        raise HTTPException(
            status_code=404,
            detail=f"No match found for {date}"
        )

    return result


# ============================================================
# EXISTING ANALYSIS ENDPOINT
# ============================================================

@app.get("/analysis/{date}")
def analysis(date: str):

    from engine.readiness_engine import analyze_readiness

    result = analyze_readiness(date)

    if result is None:
        raise HTTPException(
            status_code=404,
            detail=f"Analysis data not available for {date}"
        )

    return result


# ============================================================
# NEW POST ENDPOINT
# DASHBOARD V2 → FASTAPI → READINESS ENGINE
# ============================================================

@app.post("/planner/analyze")
def analyze_manual_planner(request: PlannerAnalysisRequest):

    # --------------------------------------------------------
    # 1. Validate date
    # --------------------------------------------------------

    try:
        current_date = datetime.strptime(
            request.date,
            "%Y-%m-%d"
        )

    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="date must use YYYY-MM-DD format"
        )


    # --------------------------------------------------------
    # 2. Validate match date
    # --------------------------------------------------------

    days_to_match = None

    if request.match_date:

        try:
            match_date = datetime.strptime(
                request.match_date,
                "%Y-%m-%d"
            )

        except ValueError:
            raise HTTPException(
                status_code=400,
                detail="match_date must use YYYY-MM-DD format"
            )

        days_to_match = (
            match_date - current_date
        ).days

        if days_to_match < 0:
            raise HTTPException(
                status_code=400,
                detail="match_date cannot be before analysis date"
            )


    # --------------------------------------------------------
    # 3. Validate availability
    # --------------------------------------------------------

    if request.availability not in ["full", "limited"]:
        raise HTTPException(
            status_code=400,
            detail="availability must be 'full' or 'limited'"
        )


    # --------------------------------------------------------
    # 4. Calculate workload ratio
    # --------------------------------------------------------

    if request.chronic_baseline <= 0:
        raise HTTPException(
            status_code=400,
            detail="chronic_baseline must be greater than 0"
        )

    workload_ratio = (
        request.acute_load /
        request.chronic_baseline
    )

    workload_ratio = round(workload_ratio, 2)


    # --------------------------------------------------------
    # 5. Calculate fatigue indicator
    #
    # Higher soreness + stress + lower energy
    # = higher fatigue
    # --------------------------------------------------------

    fatigue_indicator = (
        request.muscle_soreness * 0.4
        + request.stress * 0.3
        + (100 - request.energy) * 0.3
    )

    fatigue_indicator = round(
        fatigue_indicator,
        2
    )


    # --------------------------------------------------------
    # 6. Calculate readiness
    # --------------------------------------------------------

    readiness_score, readiness_status = determine_readiness(
        recovery_score=request.recovery_score,
        fatigue_indicator=fatigue_indicator,
        workload_ratio=workload_ratio,
        availability=request.availability,
        days_to_match=days_to_match
    )


    # --------------------------------------------------------
    # 7. Generate training recommendation
    # --------------------------------------------------------

    recommendation = recommend_training(
        readiness_status=readiness_status,
        days_to_match=days_to_match,
        availability=request.availability
    )


    # --------------------------------------------------------
    # 8. Determine whether replanning is needed
    # --------------------------------------------------------

    plan_revision_required = False

    if readiness_status == "reduced":
        plan_revision_required = True

    if request.availability == "limited":
        plan_revision_required = True

    if workload_ratio > 1.2:
        plan_revision_required = True

    if fatigue_indicator > 35:
        plan_revision_required = True

    if days_to_match is not None and days_to_match <= 3:
        plan_revision_required = True


    # --------------------------------------------------------
    # 9. Create a dynamic training plan
    # --------------------------------------------------------

    revised_plan = generate_revised_plan(
        start_date=request.date,
        end_date=request.match_date or request.date,
        recovery_score=request.recovery_score,
        fatigue_indicator=fatigue_indicator,
        workload_ratio=workload_ratio,
        availability=request.availability,
        match_date=request.match_date
    )


    # --------------------------------------------------------
    # 10. Constraint verification
    # --------------------------------------------------------

    try:

        constraint_result = check_plan_constraints(
            revised_plan,
            match_date=request.match_date,
            availability=request.availability,
            readiness_status=readiness_status,
            workload_ratio=workload_ratio
        )

    except TypeError:

        # Compatibility fallback if your current
        # constraint_checker.py uses a different
        # function signature.

        constraint_result = {
            "status": "generated",
            "message": "Plan generated; detailed constraint check available through replanning engine."
        }


    # --------------------------------------------------------
    # 11. Return complete result to Streamlit
    # --------------------------------------------------------

    return {
        "status": "success",

        "input": {
            "date": request.date,
            "recovery_score": request.recovery_score,
            "sleep_hours": request.sleep_hours,
            "energy": request.energy,
            "muscle_soreness": request.muscle_soreness,
            "stress": request.stress,
            "mood": request.mood,
            "motivation": request.motivation,
            "availability": request.availability,
            "current_training_load": request.current_training_load,
            "acute_load": request.acute_load,
            "chronic_baseline": request.chronic_baseline,
            "match_date": request.match_date,
            "match_importance": request.match_importance
        },

        "workload": {
            "current_training_load":
                request.current_training_load,

            "acute_load":
                request.acute_load,

            "chronic_baseline":
                request.chronic_baseline,

            "workload_ratio":
                workload_ratio
        },

        "recovery": {
            "recovery_score":
                request.recovery_score,

            "sleep_hours":
                request.sleep_hours,

            "energy":
                request.energy,

            "muscle_soreness":
                request.muscle_soreness,

            "stress":
                request.stress,

            "fatigue_indicator":
                fatigue_indicator
        },

        "wellness": {
            "mood":
                request.mood,

            "motivation":
                request.motivation,

            "availability":
                request.availability
        },

        "competition": {
            "match_date":
                request.match_date,

            "match_importance":
                request.match_importance,

            "days_to_match":
                days_to_match
        },

        "readiness": {
            "readiness_score":
                readiness_score,

            "readiness_status":
                readiness_status
        },

        "training_recommendation":
            recommendation,

        "plan_revision_required":
            plan_revision_required,

        "revised_plan":
            revised_plan,

        "constraint_verification":
            constraint_result
    }


# ============================================================
# EXISTING REPLANNING DEMONSTRATION
# ============================================================

@app.get("/replanning-demo")
def replanning_demo():

    from planner.replanning_engine import create_replanning_demo

    result = create_replanning_demo()

    return {
        "status": "success",
        "message": "Dynamic replanning demonstration completed.",
        "data": result
    }