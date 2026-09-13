import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
from datetime import date


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Athlete Performance AI",
    page_icon="🏃",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

    /* Main background */
    .stApp {
        background: linear-gradient(
            135deg,
            #07111f 0%,
            #0b1728 45%,
            #101827 100%
        );
        color: #ffffff;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: linear-gradient(
            180deg,
            #081525 0%,
            #0d1b2e 100%
        );
        border-right: 1px solid #24344d;
    }

    /* Main title */
    .main-title {
        font-size: 42px;
        font-weight: 800;
        margin-bottom: 0px;
        background: linear-gradient(
            90deg,
            #00e5ff,
            #7c4dff,
            #ff4ecd
        );
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .subtitle {
        color: #9fb0c8;
        font-size: 16px;
        margin-bottom: 25px;
    }

    /* Cards */
    .metric-card {
        background: linear-gradient(
            145deg,
            #101f34,
            #0b1627
        );
        border: 1px solid #263a55;
        border-radius: 16px;
        padding: 20px;
        min-height: 125px;
        box-shadow: 0 8px 25px rgba(0,0,0,0.25);
    }

    .metric-title {
        color: #91a4bd;
        font-size: 14px;
        font-weight: 600;
    }

    .metric-value {
        color: #ffffff;
        font-size: 30px;
        font-weight: 800;
        margin-top: 8px;
    }

    .metric-small {
        color: #7f93ad;
        font-size: 12px;
    }

    /* Section titles */
    .section-title {
        font-size: 24px;
        font-weight: 750;
        color: #ffffff;
        margin-top: 25px;
        margin-bottom: 15px;
    }

    /* Recommendation */
    .recommendation {
        background: linear-gradient(
            135deg,
            #18284b,
            #151d38
        );
        border: 1px solid #3e5c91;
        border-radius: 18px;
        padding: 25px;
        box-shadow: 0 8px 30px rgba(0,0,0,0.25);
    }

    .recommendation-title {
        font-size: 14px;
        color: #8fa7c6;
    }

    .recommendation-value {
        font-size: 25px;
        font-weight: 800;
        color: #ffffff;
    }

    /* Status */
    .status-high {
        background: rgba(0, 230, 118, 0.12);
        border: 1px solid #00e676;
        color: #00e676;
        padding: 15px;
        border-radius: 14px;
        font-weight: 700;
    }

    .status-moderate {
        background: rgba(255, 193, 7, 0.12);
        border: 1px solid #ffc107;
        color: #ffc107;
        padding: 15px;
        border-radius: 14px;
        font-weight: 700;
    }

    .status-reduced {
        background: rgba(255, 82, 82, 0.12);
        border: 1px solid #ff5252;
        color: #ff5252;
        padding: 15px;
        border-radius: 14px;
        font-weight: 700;
    }

    /* Replanning */
    .replan-card {
        background: linear-gradient(
            135deg,
            #211933,
            #17162a
        );
        border: 1px solid #704d9b;
        border-radius: 18px;
        padding: 22px;
    }

    /* Input labels */
    label {
        color: #c6d3e4 !important;
    }

    /* Button */
    .stButton > button {
        width: 100%;
        border-radius: 12px;
        border: 1px solid #00bcd4;
        background: linear-gradient(
            90deg,
            #006d77,
            #7c4dff
        );
        color: white;
        font-weight: 750;
        padding: 12px;
    }

    .stButton > button:hover {
        border: 1px solid #ffffff;
        transform: scale(1.01);
    }

    /* Dataframe */
    [data-testid="stDataFrame"] {
        border-radius: 12px;
        overflow: hidden;
    }

</style>
""", unsafe_allow_html=True)


# ============================================================
# API
# ============================================================

import os

API_URL = os.getenv(
    "API_URL",
    "http://127.0.0.1:8000"
)

# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="main-title">🏃 Athlete Performance AI</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Autonomous workload • recovery • readiness • dynamic planning'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.markdown("## 🎛️ Athlete Control Panel")

st.sidebar.markdown("---")


# ------------------------------------------------------------
# Competition
# ------------------------------------------------------------

st.sidebar.markdown("### 🏆 Competition")

analysis_date = st.sidebar.date_input(
    "Analysis Date",
    value=date(2026, 9, 12)
)

match_date = st.sidebar.date_input(
    "Next Match Date",
    value=date(2026, 9, 15)
)

match_importance = st.sidebar.selectbox(
    "Match Importance",
    ["low", "medium", "high"],
    index=2
)


# ------------------------------------------------------------
# Workload
# ------------------------------------------------------------

st.sidebar.markdown("### 📊 Workload")

current_training_load = st.sidebar.number_input(
    "Current Training Load",
    min_value=0.0,
    max_value=5000.0,
    value=590.0,
    step=10.0
)

acute_load = st.sidebar.number_input(
    "Acute Load",
    min_value=0.0,
    max_value=10000.0,
    value=1720.0,
    step=10.0
)

chronic_baseline = st.sidebar.number_input(
    "Chronic Baseline",
    min_value=1.0,
    max_value=5000.0,
    value=560.0,
    step=10.0
)


# ------------------------------------------------------------
# Recovery
# ------------------------------------------------------------

st.sidebar.markdown("### 😴 Recovery")

recovery_score = st.sidebar.number_input(
    "Recovery Score",
    min_value=0,
    max_value=100,
    value=52,
    step=1
)

sleep_hours = st.sidebar.number_input(
    "Sleep Hours",
    min_value=0.0,
    max_value=24.0,
    value=6.2,
    step=0.1
)

energy = st.sidebar.number_input(
    "Energy",
    min_value=0,
    max_value=100,
    value=55,
    step=1
)

muscle_soreness = st.sidebar.number_input(
    "Muscle Soreness",
    min_value=0,
    max_value=100,
    value=62,
    step=1
)

stress = st.sidebar.number_input(
    "Stress",
    min_value=0,
    max_value=100,
    value=68,
    step=1
)


# ------------------------------------------------------------
# Wellness
# ------------------------------------------------------------

st.sidebar.markdown("### 🧠 Wellness")

mood = st.sidebar.number_input(
    "Mood",
    min_value=0,
    max_value=100,
    value=58,
    step=1
)

motivation = st.sidebar.number_input(
    "Motivation",
    min_value=0,
    max_value=100,
    value=62,
    step=1
)

availability = st.sidebar.selectbox(
    "Availability",
    ["full", "limited"]
)


st.sidebar.markdown("---")


# ============================================================
# ANALYZE BUTTON
# ============================================================

analyze_button = st.sidebar.button(
    "🚀 ANALYZE ATHLETE",
    use_container_width=True
)


# ============================================================
# API FUNCTION
# ============================================================

def analyze_athlete():

    payload = {
        "date": analysis_date.strftime("%Y-%m-%d"),

        "recovery_score": recovery_score,
        "sleep_hours": sleep_hours,
        "energy": energy,
        "muscle_soreness": muscle_soreness,
        "stress": stress,

        "mood": mood,
        "motivation": motivation,

        "availability": availability,

        "current_training_load": current_training_load,
        "acute_load": acute_load,
        "chronic_baseline": chronic_baseline,

        "match_date": match_date.strftime("%Y-%m-%d"),
        "match_importance": match_importance
    }

    try:

        response = requests.post(
            f"{API_URL}/planner/analyze",
            json=payload,
            timeout=10
        )

        if response.status_code == 200:
            return response.json()

        st.error(
            f"FastAPI Error {response.status_code}: "
            f"{response.text}"
        )

        return None

    except requests.exceptions.ConnectionError:

        st.error(
            "❌ FastAPI is not running. Start it with:\n\n"
            "`uvicorn main:app --reload`"
        )

        return None

    except Exception as e:

        st.error(f"❌ Error: {e}")

        return None


# ============================================================
# RUN ANALYSIS
# ============================================================

if analyze_button:

    with st.spinner(
        "⚡ Processing workload, recovery and competition data..."
    ):

        result = analyze_athlete()

    if result:

        st.session_state["analysis_result"] = result


# ============================================================
# EMPTY STATE
# ============================================================

if "analysis_result" not in st.session_state:

    st.markdown(
        """
        <div style="
            margin-top:40px;
            padding:45px;
            text-align:center;
            background:linear-gradient(135deg,#101f34,#111a2c);
            border:1px solid #2b405d;
            border-radius:20px;
        ">

        <div style="font-size:55px;">🏃</div>

        <h2 style="color:white;">
        Athlete Performance Control Center
        </h2>

        <p style="color:#91a4bd;font-size:16px;">
        Enter the athlete's current workload, recovery and wellness
        values from the control panel and run the analysis.
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )

    st.stop()


# ============================================================
# RESULT
# ============================================================

result = st.session_state["analysis_result"]

readiness = result.get("readiness", {})
workload = result.get("workload", {})
recovery = result.get("recovery", {})
wellness = result.get("wellness", {})
competition = result.get("competition", {})


readiness_score = readiness.get(
    "readiness_score",
    0
)

readiness_status = readiness.get(
    "readiness_status",
    "unknown"
)

workload_ratio = workload.get(
    "workload_ratio",
    0
)

fatigue_indicator = recovery.get(
    "fatigue_indicator",
    0
)

days_to_match = competition.get(
    "days_to_match",
    None
)


# ============================================================
# TOP METRICS
# ============================================================

st.markdown(
    '<div class="section-title">📡 Live Performance Overview</div>',
    unsafe_allow_html=True
)

c1, c2, c3, c4 = st.columns(4)


with c1:

    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-title">READINESS SCORE</div>
            <div class="metric-value">{readiness_score}/100</div>
            <div class="metric-small">Current performance readiness</div>
        </div>
        """,
        unsafe_allow_html=True
    )


with c2:

    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-title">WORKLOAD RATIO</div>
            <div class="metric-value">{workload_ratio:.2f}</div>
            <div class="metric-small">Acute / chronic workload</div>
        </div>
        """,
        unsafe_allow_html=True
    )


with c3:

    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-title">FATIGUE INDEX</div>
            <div class="metric-value">{fatigue_indicator:.1f}</div>
            <div class="metric-small">Synthetic fatigue indicator</div>
        </div>
        """,
        unsafe_allow_html=True
    )


with c4:

    match_text = (
        f"{days_to_match} days"
        if days_to_match is not None
        else "N/A"
    )

    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-title">NEXT COMPETITION</div>
            <div class="metric-value">{match_text}</div>
            <div class="metric-small">
                {competition.get("match_date", "N/A")}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# READINESS STATUS
# ============================================================

st.markdown(
    '<div class="section-title">🧠 Readiness Status</div>',
    unsafe_allow_html=True
)


if readiness_status == "high":

    st.markdown(
        f"""
        <div class="status-high">
        🟢 HIGH READINESS — {readiness_score}/100
        </div>
        """,
        unsafe_allow_html=True
    )

elif readiness_status == "moderate":

    st.markdown(
        f"""
        <div class="status-moderate">
        🟡 MODERATE READINESS — {readiness_score}/100
        </div>
        """,
        unsafe_allow_html=True
    )

else:

    st.markdown(
        f"""
        <div class="status-reduced">
        🔴 REDUCED READINESS — {readiness_score}/100
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# WORKLOAD + RECOVERY
# ============================================================

left, right = st.columns(2)


# ------------------------------------------------------------
# Workload chart
# ------------------------------------------------------------

with left:

    st.markdown(
        '<div class="section-title">📊 Workload Monitor</div>',
        unsafe_allow_html=True
    )

    workload_df = pd.DataFrame({
        "Metric": [
            "Current Load",
            "Acute Load",
            "Chronic Baseline"
        ],
        "Value": [
            current_training_load,
            acute_load,
            chronic_baseline
        ]
    })

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=workload_df["Metric"],
            y=workload_df["Value"],
            text=workload_df["Value"],
            textposition="outside"
        )
    )

    fig.update_layout(
        template="plotly_dark",
        height=350,
        margin=dict(l=20, r=20, t=30, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        showlegend=False
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ------------------------------------------------------------
# Recovery
# ------------------------------------------------------------

with right:

    st.markdown(
        '<div class="section-title">😴 Recovery Monitor</div>',
        unsafe_allow_html=True
    )

    r1, r2 = st.columns(2)

    with r1:

        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-title">RECOVERY</div>
                <div class="metric-value">
                    {recovery.get("recovery_score", recovery_score)}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with r2:

        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-title">SLEEP</div>
                <div class="metric-value">
                    {recovery.get("sleep_hours", sleep_hours):.1f}h
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    r3, r4 = st.columns(2)

    with r3:

        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-title">ENERGY</div>
                <div class="metric-value">
                    {recovery.get("energy", energy)}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with r4:

        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-title">STRESS</div>
                <div class="metric-value">
                    {recovery.get("stress", stress)}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )


# ============================================================
# WELLNESS
# ============================================================

st.markdown(
    '<div class="section-title">🧠 Wellness Dashboard</div>',
    unsafe_allow_html=True
)

w1, w2, w3, w4 = st.columns(4)


with w1:

    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-title">Mood</div>
            <div class="metric-value">
                {wellness.get("mood", mood)}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


with w2:

    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-title">Motivation</div>
            <div class="metric-value">
                {wellness.get("motivation", motivation)}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


with w3:

    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-title">Availability</div>
            <div class="metric-value">
                {wellness.get("availability", availability).upper()}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
        


with w4:

    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-title">Soreness</div>
            <div class="metric-value">
                {recovery.get("muscle_soreness", muscle_soreness)}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    


# ============================================================
# COMPETITION
# ============================================================

st.markdown(
    '<div class="section-title">🏆 Competition Intelligence</div>',
    unsafe_allow_html=True
)

comp1, comp2, comp3 = st.columns(3)


with comp1:

    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-title">NEXT MATCH</div>
            <div class="metric-value">
                {competition.get("match_date", "N/A")}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


with comp2:

    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-title">DAYS REMAINING</div>
            <div class="metric-value">
                {days_to_match if days_to_match is not None else "N/A"}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


with comp3:

    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-title">IMPORTANCE</div>
            <div class="metric-value">
                {competition.get("match_importance",
                match_importance).upper()}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# TRAINING RECOMMENDATION
# ============================================================

st.markdown(
    '<div class="section-title">🏋️ Training Recommendation</div>',
    unsafe_allow_html=True
)

recommendation = result.get(
    "training_recommendation",
    {}
)

t1, t2, t3 = st.columns(3)


with t1:

    st.markdown(
        f"""
        <div class="recommendation">
            <div class="recommendation-title">
                TRAINING TYPE
            </div>
            <div class="recommendation-value">
                {recommendation.get("training_type", "N/A")}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


with t2:

    st.markdown(
        f"""
        <div class="recommendation">
            <div class="recommendation-title">
                INTENSITY
            </div>
            <div class="recommendation-value">
                {recommendation.get("intensity", "N/A").upper()}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


with t3:

    st.markdown(
        f"""
        <div class="recommendation">
            <div class="recommendation-title">
                TARGET LOAD
            </div>
            <div class="recommendation-value">
                {recommendation.get("target_load", "N/A").upper()}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# AUTONOMOUS REPLANNING
# ============================================================

st.markdown(
    '<div class="section-title">🔄 Autonomous Replanning</div>',
    unsafe_allow_html=True
)

revision_required = result.get(
    "plan_revision_required",
    False
)

if revision_required:

    st.markdown(
        """
        <div class="replan-card">
            <h3 style="color:#ffca28;">
            🔄 PLAN REVISION REQUIRED
            </h3>

            
            The current athlete state has triggered a dynamic
            plan recalculation.
            

       
            The planner has generated an updated training plan
            using the latest workload, recovery, availability
            and competition inputs.
            
        </div>
        """,
        unsafe_allow_html=True
    )

else:

    st.success(
        "✅ Current plan remains suitable under the current "
        "demonstration rules."
    )


# ============================================================
# REVISED PLAN
# ============================================================

st.markdown(
    '<div class="section-title">📅 Generated Training Plan</div>',
    unsafe_allow_html=True
)

revised_plan = result.get(
    "revised_plan",
    None
)

if revised_plan:

    if isinstance(revised_plan, dict):

        sessions = revised_plan.get(
            "sessions",
            revised_plan.get(
                "plan",
                revised_plan.get(
                    "training_plan",
                    []
                )
            )
        )

        if isinstance(sessions, list) and sessions:

            rows = []

            for session in sessions:

                if isinstance(session, dict):
                    rows.append(session)

            if rows:

                df = pd.DataFrame(rows)

                st.dataframe(
                    df,
                    use_container_width=True,
                    hide_index=True
                )

        else:

            st.json(revised_plan)

    elif isinstance(revised_plan, list):

        rows = [
            x for x in revised_plan
            if isinstance(x, dict)
        ]

        if rows:

            st.dataframe(
                pd.DataFrame(rows),
                use_container_width=True,
                hide_index=True
            )

        else:

            st.write(revised_plan)

    else:

        st.write(revised_plan)

else:

    st.info(
        "No revised plan was returned."
    )



# ============================================================
# RAW RESPONSE
# ============================================================

with st.expander("🔎 Developer: View API Response"):

    st.json(result)


# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

st.caption(
    "Autonomous Athlete Performance Planner • "
    "Synthetic research/demo environment"
)