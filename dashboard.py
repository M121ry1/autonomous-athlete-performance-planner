import requests
import streamlit as st
import pandas as pd
import plotly.graph_objects as go


# ============================================================
# CONFIGURATION
# ============================================================

API_URL = "http://127.0.0.1:8000"


st.set_page_config(
    page_title="Autonomous Athlete Performance Planner",
    page_icon="🏃",
    layout="wide"
)


# ============================================================
# HEADER
# ============================================================

st.title("🏃 Autonomous Athlete Performance Planner")

st.markdown(
    """
    **Synthetic performance-planning research dashboard**

    The system analyzes workload, recovery, wellness and
    competition schedule to generate and revise training plans.
    """
)

st.divider()


# ============================================================
# API HELPER
# ============================================================

def get_api_data(endpoint):

    try:

        response = requests.get(
            f"{API_URL}{endpoint}",
            timeout=5
        )

        response.raise_for_status()

        return response.json()

    except requests.exceptions.RequestException as error:

        st.error(
            f"Unable to connect to FastAPI: {error}"
        )

        return None


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.header("Dashboard Controls")

analysis_date = st.sidebar.selectbox(
    "Select analysis date",
    [
        "2026-09-08",
        "2026-09-09",
        "2026-09-10",
        "2026-09-11",
        "2026-09-12"
    ],
    index=3
)


if st.sidebar.button(
    "🔄 Refresh Analysis",
    use_container_width=True
):

    st.rerun()


# ============================================================
# LOAD ANALYSIS
# ============================================================

analysis_response = get_api_data(
    f"/analysis/{analysis_date}"
)


if analysis_response is None:

    st.stop()


analysis = analysis_response.get(
    "analysis",
    analysis_response
)


# ============================================================
# EXTRACT DATA
# ============================================================

workload = analysis.get(
    "workload",
    {}
)

recovery = analysis.get(
    "recovery",
    {}
)

wellness = analysis.get(
    "wellness",
    {}
)

next_match = analysis.get(
    "next_match"
)

readiness_score = analysis.get(
    "readiness_score",
    0
)

readiness_status = analysis.get(
    "readiness_status",
    "unknown"
)

training_recommendation = analysis.get(
    "training_recommendation",
    {}
)


# ============================================================
# TOP METRICS
# ============================================================

st.subheader(
    f"📊 Athlete Status — {analysis_date}"
)

col1, col2, col3, col4, col5 = st.columns(5)


col1.metric(
    "Readiness Score",
    readiness_score
)

col2.metric(
    "Recovery Score",
    recovery.get(
        "recovery_score",
        "N/A"
    )
)

col3.metric(
    "Acute Load",
    workload.get(
        "acute_load",
        "N/A"
    )
)

col4.metric(
    "Workload Ratio",
    workload.get(
        "workload_ratio",
        "N/A"
    )
)

col5.metric(
    "Fatigue Indicator",
    recovery.get(
        "fatigue_indicator",
        "N/A"
    )
)


st.divider()


# ============================================================
# STATUS
# ============================================================

left, right = st.columns(2)


with left:

    st.subheader("🧠 Readiness")

    st.write(
        f"**Status:** {readiness_status.upper()}"
    )

    st.progress(
        min(
            max(
                int(readiness_score),
                0
            ),
            100
        )
    )

    st.write(
        f"Readiness score: **{readiness_score}/100**"
    )


with right:

    st.subheader("🏋️ Training Recommendation")

    st.info(
        training_recommendation.get(
            "training_type",
            "No recommendation"
        )
    )

    st.write(
        "**Intensity:** "
        + str(
            training_recommendation.get(
                "intensity",
                "N/A"
            )
        )
    )

    st.write(
        "**Target Load:** "
        + str(
            training_recommendation.get(
                "target_load",
                "N/A"
            )
        )
    )


st.divider()


# ============================================================
# WORKLOAD ANALYSIS
# ============================================================

st.subheader("📈 Workload Analysis")

workload_col1, workload_col2, workload_col3 = st.columns(3)


with workload_col1:

    st.metric(
        "Acute Load",
        workload.get(
            "acute_load",
            "N/A"
        )
    )


with workload_col2:

    st.metric(
        "Chronic Baseline",
        workload.get(
            "chronic_baseline",
            "N/A"
        )
    )


with workload_col3:

    st.metric(
        "Workload Ratio",
        workload.get(
            "workload_ratio",
            "N/A"
        )
    )


# ============================================================
# WORKLOAD CHART
# ============================================================

gps_data = get_api_data("/gps/")


if gps_data:

    gps_df = pd.DataFrame(gps_data)

    if "date" in gps_df.columns:

        fig = go.Figure()

        fig.add_trace(
            go.Scatter(
                x=gps_df["date"],
                y=gps_df["training_load"],
                mode="lines+markers",
                name="Training Load"
            )
        )

        fig.update_layout(
            title="Training Load Over Time",
            xaxis_title="Date",
            yaxis_title="Training Load",
            height=400
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


st.divider()


# ============================================================
# RECOVERY & WELLNESS
# ============================================================

st.subheader("💤 Recovery & Wellness")

recovery_col1, recovery_col2, recovery_col3, recovery_col4 = st.columns(4)


with recovery_col1:

    st.metric(
        "Recovery",
        recovery.get(
            "recovery_score",
            "N/A"
        )
    )


with recovery_col2:

    st.metric(
        "Sleep",
        f"{recovery.get('sleep_hours', 'N/A')} hrs"
    )


with recovery_col3:

    st.metric(
        "Energy",
        wellness.get(
            "energy",
            "N/A"
        )
    )


with recovery_col4:

    st.metric(
        "Stress",
        wellness.get(
            "stress",
            "N/A"
        )
    )


st.divider()


# ============================================================
# COMPETITION
# ============================================================

st.subheader("🏆 Competition Schedule")

if next_match:

    match_col1, match_col2, match_col3, match_col4 = st.columns(4)

    with match_col1:

        st.metric(
            "Next Match",
            next_match.get(
                "date",
                "N/A"
            )
        )

    with match_col2:

        st.metric(
            "Opponent",
            next_match.get(
                "opponent",
                "N/A"
            )
        )

    with match_col3:

        st.metric(
            "Importance",
            next_match.get(
                "importance",
                "N/A"
            )
        )

    with match_col4:

        st.metric(
            "Days Away",
            analysis.get(
                "days_to_next_match",
                "N/A"
            )
        )

else:

    st.info(
        "No upcoming match found."
    )


st.divider()


# ============================================================
# AUTONOMOUS REPLANNING
# ============================================================

st.header(
    "🤖 Autonomous Replanning"
)

st.markdown(
    """
    The system can regenerate the training plan when athlete
    state or competition conditions change.
    """
)


if st.button(
    "🚀 Run Replanning Demonstration",
    use_container_width=True
):

    with st.spinner(
        "Running autonomous replanning..."
    ):

        replanning_response = get_api_data(
            "/replanning-demo"
        )

    if replanning_response:

        replanning = replanning_response.get(
            "replanning",
            {}
        )

        # ----------------------------------------------------
        # Initial plan
        # ----------------------------------------------------

        st.subheader(
            "1️⃣ Initial Plan"
        )

        initial = replanning.get(
            "initial_plan",
            {}
        )

        st.write(
            f"Readiness Score: **{initial.get('readiness_score', 'N/A')}**"
        )

        st.write(
            f"Readiness Status: **{initial.get('readiness_status', 'N/A')}**"
        )

        # ----------------------------------------------------
        # Revision 1
        # ----------------------------------------------------

        st.subheader(
            "2️⃣ Revision #1 — Athlete State Changed"
        )

        revision_1 = replanning.get(
            "revision_1",
            {}
        )

        st.write(
            f"Readiness Score: **{revision_1.get('readiness_score', 'N/A')}**"
        )

        st.write(
            f"Readiness Status: **{revision_1.get('readiness_status', 'N/A')}**"
        )

        # ----------------------------------------------------
        # Revision 2
        # ----------------------------------------------------

        st.subheader(
            "3️⃣ Revision #2 — Match Schedule Changed"
        )

        revision_2 = replanning.get(
            "revision_2",
            {}
        )

        st.write(
            f"Readiness Score: **{revision_2.get('readiness_score', 'N/A')}**"
        )

        st.write(
            f"Readiness Status: **{revision_2.get('readiness_status', 'N/A')}**"
        )

        st.write(
            f"Updated Match Date: **{revision_2.get('match_date', 'N/A')}**"
        )

        # ----------------------------------------------------
        # Constraint verification
        # ----------------------------------------------------

        st.subheader(
            "4️⃣ Constraint Verification"
        )

        checks = [
            (
                "Initial Plan",
                initial.get(
                    "constraint_check",
                    {}
                )
            ),
            (
                "Revision #1",
                revision_1.get(
                    "constraint_check",
                    {}
                )
            ),
            (
                "Revision #2",
                revision_2.get(
                    "constraint_check",
                    {}
                )
            )
        ]

        for name, result in checks:

            passed = result.get(
                "constraints_passed",
                False
            )

            if passed:

                st.success(
                    f"{name}: Constraints PASSED ✅"
                )

            else:

                st.error(
                    f"{name}: Constraint violations detected ❌"
                )

                for violation in result.get(
                    "violations",
                    []
                ):

                    st.write(
                        f"- {violation}"
                    )


st.divider()


# ============================================================
# SYSTEM STATUS
# ============================================================

st.subheader("⚙️ System Status")

status_col1, status_col2, status_col3 = st.columns(3)


with status_col1:

    st.success(
        "FastAPI Backend: Connected"
    )


with status_col2:

    st.success(
        "Analysis Engine: Active"
    )


with status_col3:

    st.success(
        "Planning Engine: Active"
    )


st.caption(
    "This dashboard uses synthetic performance-planning "
    "data for research and demonstration. "
    "Readiness and workload values are project-specific "
    "planning metrics and are not medical assessments."
)