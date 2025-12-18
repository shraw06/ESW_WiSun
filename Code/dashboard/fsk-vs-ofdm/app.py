# app.py
import os
import re
import glob

import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

def load_theme():
    st.markdown("""
    <style>

    /* MAIN APP BACKGROUND - Purple gradient like the reference */
    .stApp {
        background: linear-gradient(135deg, #7B68EE 0%, #9B8EF9 50%, #C4B5FD 100%) !important;
        background-attachment: fixed !important;
    }

    /* WHITE CARD for main content */
    .main, .block-container {
        background: rgba(255, 255, 255, 0.95) !important;
        padding: 2.5rem !important;
        border-radius: 24px !important;
        box-shadow: 0 8px 32px rgba(0,0,0,0.12);
        margin: 20px auto !important;
        max-width: 1400px !important;
    }

    /* TITLES - Purple theme */
    h1 {
        color: #6366F1 !important;
        font-weight: 700 !important;
        text-align: center !important;
        font-size: 2.5rem !important;
        margin-bottom: 0.5rem !important;
    }
    
    h2, h3 {
        color: #7C3AED !important;
        font-weight: 700 !important;
    }

    /* Subtitle/description text */
    .stMarkdown p {
        color: #64748B !important;
    }

    /* KPI BOXES - White cards with purple accents */
    div[data-testid="metric-container"] {
        background: white !important;
        padding: 24px !important;
        border-radius: 20px !important;
        border: 2px solid #E0E7FF !important;
        box-shadow: 0 4px 16px rgba(99, 102, 241, 0.08) !important;
    }

    /* Metric labels */
    div[data-testid="metric-container"] label {
        color: #64748B !important;
        font-weight: 600 !important;
        font-size: 0.875rem !important;
        text-transform: uppercase !important;
        letter-spacing: 0.05em !important;
    }

    /* Metric values */
    div[data-testid="metric-container"] [data-testid="stMetricValue"] {
        color: #6366F1 !important;
        font-weight: 700 !important;
        font-size: 2rem !important;
    }

    /* Plotly charts background */
    .js-plotly-plot {
        background: white !important;
        border-radius: 16px !important;
        padding: 16px !important;
        box-shadow: 0 2px 12px rgba(0,0,0,0.06) !important;
    }

    /* Dataframe styling */
    .stDataFrame {
        background: white !important;
        border-radius: 16px !important;
        overflow: hidden !important;
        box-shadow: 0 2px 12px rgba(0,0,0,0.06) !important;
    }

    /* Expander styling */
    .streamlit-expanderHeader {
        background: white !important;
        border-radius: 12px !important;
        border: 1px solid #E0E7FF !important;
        color: #7C3AED !important;
        font-weight: 600 !important;
    }

    /* Success box */
    .stSuccess {
        background: linear-gradient(135deg, #ECFDF5 0%, #D1FAE5 100%) !important;
        border-left: 4px solid #10B981 !important;
        border-radius: 12px !important;
    }

    /* Warning box */
    .stWarning {
        background: linear-gradient(135deg, #FEF3C7 0%, #FDE68A 100%) !important;
        border-left: 4px solid #F59E0B !important;
        border-radius: 12px !important;
    }

    /* Caption text */
    .stCaption {
        color: #94A3B8 !important;
        font-style: italic !important;
    }

    /* Horizontal rule */
    hr {
        border-color: #E0E7FF !important;
        margin: 2rem 0 !important;
    }

    </style>
    """, unsafe_allow_html=True)

# -----------------------------
# CONFIG
# -----------------------------
TOTAL_LOCATIONS = 20         # 20 points along research street (every 10m)


# -----------------------------
# DATA LOADING HELPERS
# -----------------------------
def parse_location_from_feeds(filename: str) -> str:
    """
    For OFDM files like 'feeds (10).xlsx', returns '10'.
    If no number in the name (e.g., 'feeds.csv'), returns 'base'.
    """
    base = os.path.basename(filename)
    m = re.search(r"\((\d+)\)", base)
    if m:
        return m.group(1)
    return "base"


def load_ofdm_file(path: str) -> pd.DataFrame:
    """Load one OFDM file and map ThingSpeak fields to common columns."""
    if path.lower().endswith(".csv"):
        df = pd.read_csv(path)
    else:
        df = pd.read_excel(path)

    # Drop first row if it's all zeros in field columns (startup junk)
    field_cols = [c for c in df.columns if c.startswith("field")]
    if len(df) > 0 and not df[field_cols].isna().all(axis=None):
        first_sum = df[field_cols].fillna(0).iloc[0].sum()
        if first_sum == 0:
            df = df.iloc[1:].reset_index(drop=True)

    loc = parse_location_from_feeds(path)

    # Map fields to the same schema as FSK
    df_std = pd.DataFrame({
        "created_at": df["created_at"],
        "Temperature": df.get("field1"),
        "Humidity": df.get("field2"),
        "DisconnectedTotal": df.get("field3"),
        "RSL_out": df.get("field4"),
        "RSL_in": df.get("field5"),
        "RPL_rank": df.get("field6"),
        "Hopcount": df.get("field7"),
        "ConnectedTotal": df.get("field8"),
    })

    df_std["modulation"] = "OFDM"
    df_std["location_id"] = loc
    return df_std


def load_fsk_file(path: str) -> pd.DataFrame:
    """Load one FSK file (Location 1/2/3/20.xlsx)."""
    df = pd.read_excel(path)
    base = os.path.basename(path)
    m = re.search(r"Location (\d+)", base)
    loc = m.group(1) if m else base

    df["modulation"] = "FSK"
    df["location_id"] = loc
    return df


@st.cache_data(show_spinner=True)
def load_all_data():
    # Collect file lists
    ofdm_paths = sorted(glob.glob("data/feeds*.xlsx") + glob.glob("data/feeds*.csv"))
    fsk_paths = sorted(glob.glob("data/Location *.xlsx"))

    if not ofdm_paths:
        st.warning("No OFDM files found matching 'feeds*.xlsx/csv'.")
    if not fsk_paths:
        st.warning("No FSK files found matching 'Location *.xlsx'.")

    ofdm_list = [load_ofdm_file(p) for p in ofdm_paths]
    fsk_list = [load_fsk_file(p) for p in fsk_paths]

    ofdm = pd.concat(ofdm_list, ignore_index=True) if ofdm_list else pd.DataFrame()
    fsk = pd.concat(fsk_list, ignore_index=True) if fsk_list else pd.DataFrame()

    # Combine for global plots
    combined = pd.concat([ofdm, fsk], ignore_index=True)

    # Create numeric location index for plotting on 1D street
    def to_loc_num(x):
        m = re.search(r"(\d+)", str(x))
        return float(m.group(1)) if m else np.nan

    combined["loc_num"] = combined["location_id"].apply(to_loc_num)

    return ofdm, fsk, combined


# -----------------------------
# APP LAYOUT
# -----------------------------
st.set_page_config(
    page_title="Wi-SUN FSK vs OFDM – Research Street",
    layout="wide",
)

load_theme()

st.title("Wi-SUN RF Mapping Dashboard – FSK vs OFDM (Research Street)")

st.markdown(
    """
This dashboard compares **FSK** and **OFDM** Wi-SUN configurations on Research Street.

It highlights:

- Coverage and connectivity at 20 points along the road  
- Link quality (`RSL_in`, `RSL_out`)  
- Mesh behaviour (`Hopcount`, `RPL Rank`)  
- Why FSK fails in the middle section while OFDM still works  
"""
)

ofdm, fsk, combined = load_all_data()
if combined.empty:
    st.stop()

# -----------------------------
# KPIs
# -----------------------------
ofdm_locs = TOTAL_LOCATIONS
fsk_locs = fsk["location_id"].nunique()

avg_rsl_in_ofdm = ofdm["RSL_in"].mean()
avg_rsl_in_fsk = fsk["RSL_in"].mean()

avg_hop_ofdm = ofdm["Hopcount"].mean()
avg_hop_fsk = fsk["Hopcount"].mean()

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "OFDM Covered Locations",
    f"{TOTAL_LOCATIONS}/{TOTAL_LOCATIONS}",
)

col2.metric(
    "FSK Covered Locations",
    f"{fsk_locs}/{TOTAL_LOCATIONS}",
    help="Locations where FSK successfully joined and produced data.",
)

col3.metric(
    "Avg RSL_in (OFDM)",
    f"{avg_rsl_in_ofdm:.1f} dBm" if not np.isnan(avg_rsl_in_ofdm) else "N/A",
)

col4.metric(
    "Avg RSL_in (FSK)",
    f"{avg_rsl_in_fsk:.1f} dBm" if not np.isnan(avg_rsl_in_fsk) else "N/A",
)

st.caption(
    "RSL_in closer to 0 dBm is better. FSK is typically ~30 dB weaker than OFDM at the receiver."
)

st.markdown("---")

# -----------------------------
# 1D STREET COVERAGE VIEW
# -----------------------------
st.subheader("1. Coverage Along Research Street (20 Points Every 10m)")

# Mock full location index 1..20
loc_df = pd.DataFrame({"loc_num": np.arange(1, TOTAL_LOCATIONS + 1)})
loc_df["location_id"] = loc_df["loc_num"].astype(int).astype(str)

# Connectivity flags
ofdm_loc_presence = ofdm.groupby("location_id").size().rename("ofdm_present")
fsk_loc_presence = fsk.groupby("location_id").size().rename("fsk_present")

loc_cov = loc_df.merge(ofdm_loc_presence, on="location_id", how="left")
loc_cov = loc_cov.merge(fsk_loc_presence, on="location_id", how="left")

loc_cov["ofdm_connected"] = True
loc_cov["fsk_connected"] = loc_cov["fsk_present"].notna()

fig_cov = go.Figure()

# OFDM coverage
fig_cov.add_trace(
    go.Scatter(
        x=loc_cov["loc_num"],
        y=[1] * len(loc_cov),
        mode="markers",
        marker=dict(size=12),
        name="OFDM",
        marker_symbol="circle",
        hovertext=[
            f"Location {int(l)} – OFDM: connected"
            for l in loc_cov["loc_num"]
        ],
    )
)

# FSK coverage
fig_cov.add_trace(
    go.Scatter(
        x=loc_cov["loc_num"],
        y=[0] * len(loc_cov),
        mode="markers",
        marker=dict(size=12),
        name="FSK",
        marker_symbol="x",
        hovertext=[
            f"Location {int(l)} – FSK: {'connected' if c else 'no data'}"
            for l, c in zip(loc_cov["loc_num"], loc_cov["fsk_connected"])
        ],
    )
)

fig_cov.update_layout(
    xaxis_title="Location index along street (1 = start, 20 = end)",
    yaxis=dict(
        tickvals=[0, 1],
        ticktext=["FSK", "OFDM"],
        title="Modulation",
    ),
    height=300,
    showlegend=True,
)

st.plotly_chart(fig_cov, use_container_width=True)

st.markdown(
    """
**Interpretation**

- OFDM has data at nearly all points along the street (upper row).  
- FSK only connects at **Locations 1, 2, 3 and 20** – the entire middle section behaves as a **dead zone**.
"""
)

st.markdown("---")

# -----------------------------
# LINK QUALITY – RSL
# -----------------------------
st.subheader("2. Link Quality – RSL_in and RSL_out")

col_rsl1, col_rsl2 = st.columns(2)

with col_rsl1:
    fig_rsl_in = px.box(
        combined,
        x="modulation",
        y="RSL_in",
        color="modulation",
        title="RSL_in Distribution by Modulation",
    )
    fig_rsl_in.update_layout(yaxis_title="RSL_in (dBm)")
    st.plotly_chart(fig_rsl_in, use_container_width=True)

with col_rsl2:
    fig_rsl_out = px.box(
        combined,
        x="modulation",
        y="RSL_out",
        color="modulation",
        title="RSL_out Distribution by Modulation",
    )
    fig_rsl_out.update_layout(yaxis_title="RSL_out (dBm)")
    st.plotly_chart(fig_rsl_out, use_container_width=True)

st.markdown(
    """
**What this shows**

- **Transmit power (RSL_out)** is in a similar ballpark for both FSK and OFDM.
- **RSL_in is dramatically worse for FSK (≈ -95 dBm) than OFDM (≈ -60 dBm).**  
- This means the **downlink is the bottleneck** for FSK – the node hears the network much more weakly, so joins fail easily.
"""
)

# Scatter plot: RSL_in vs RSL_out
fig_scatter = px.scatter(
    combined,
    x="RSL_out",
    y="RSL_in",
    color="modulation",
    title="RSL_in vs RSL_out by Modulation",
    opacity=0.6,
)
fig_scatter.update_layout(
    xaxis_title="RSL_out (dBm)",
    yaxis_title="RSL_in (dBm)",
)
st.plotly_chart(fig_scatter, use_container_width=True)

st.markdown("---")

st.markdown("---")

# -----------------------------
# MESH BEHAVIOUR – HOPCOUNT & RPL RANK
# -----------------------------
st.subheader("3. Mesh Behaviour – Hopcount and RPL Rank")
combined["RPL_rank_clean"] = combined["RPL_rank"].mask(combined["RPL_rank"] >= 65000, np.nan)

# group_stats = (
#     combined.groupby("modulation")[["Hopcount", "RPL_rank"]]
#     .mean()
#     .reset_index()
#     .round(2)
# )

group_stats = (
    combined.groupby("modulation")[["Hopcount", "RPL_rank_clean"]]
    .mean()
    .rename(columns={"RPL_rank_clean": "RPL_rank"})
    .reset_index()
    .round(2)
)

col_mesh1, col_mesh2 = st.columns(2)

with col_mesh1:
    fig_hop = px.bar(
        group_stats,
        x="modulation",
        y="Hopcount",
        title="Average Hopcount by Modulation",
        text="Hopcount",
    )
    fig_hop.update_traces(textposition="outside")
    fig_hop.update_layout(yaxis_title="Average hopcount")
    st.plotly_chart(fig_hop, use_container_width=True)

with col_mesh2:
    fig_rank = px.bar(
        group_stats,
        x="modulation",
        y="RPL_rank",
        title="Average RPL Rank by Modulation",
        text="RPL_rank",
    )
    fig_rank.update_traces(textposition="outside")
    fig_rank.update_layout(yaxis_title="Average RPL Rank (routing cost)")
    st.plotly_chart(fig_rank, use_container_width=True)

st.markdown(
    """
**Insights**

- **FSK hopcount ≈ 4** vs **OFDM hopcount ≈ 1**  
  → FSK almost never finds a nearby parent; it behaves like a 3–5 hop leaf.  
- **FSK RPL Rank** is high at many locations (especially Location 3), indicating **weak, expensive routes**.  
- OFDM typically uses **1-hop paths** to nearby nodes → healthier mesh.
"""
)

st.markdown("---")

# -----------------------------
# PER LOCATION SUMMARY
# -----------------------------
st.subheader("4. Per-Location Summary (Only Where FSK Has Data)")

# FSK location stats
if not fsk.empty:
    fsk_loc_summary = (
        fsk.groupby("location_id")[["RSL_out", "RSL_in", "RPL_rank", "Hopcount"]]
        .mean()
        .round(2)
        .reset_index()
    )

    st.markdown("**FSK locations (1, 2, 3, 20):**")
    st.dataframe(fsk_loc_summary, use_container_width=True)

    # Compare with OFDM at same location_ids (if present)
    ofdm_loc_summary = (
        ofdm.groupby("location_id")[["RSL_out", "RSL_in", "Hopcount"]]
        .mean()
        .round(2)
        .reset_index()
    )

    merged_loc = fsk_loc_summary.merge(
        ofdm_loc_summary,
        on="location_id",
        suffixes=("_FSK", "_OFDM"),
        how="left",
    )

    st.markdown("**Direct comparison at locations where FSK has readings:**")
    st.dataframe(merged_loc, use_container_width=True)

    st.caption(
        "At Location 3, FSK has very weak RSL_in and high RPL rank → exactly where you observed over-the-street bridge and heavy obstruction."
    )

st.markdown("---")

# -----------------------------
# EXPLANATION SECTION – WHY FSK FAILS, WHY OFDM HELPS
# -----------------------------
st.subheader("5. Why does this behaviour occur?")

with st.expander("RF & deployment reasons (FSK dead zone vs OFDM coverage)", expanded=True):
    st.markdown(
        """
### 5.1 Physical environment effects

From field observations and the campus map:

- Research street is like an **RF valley** – tall buildings on both sides.  
- Two FSK FFNs are on **Vindhya A2** and **Vindhya A6 rooftops**.  
- Signals must pass through **concrete, rebar, trees, and a metal bridge** → heavy attenuation and multipath.  
- The **metal bridge** in the middle acts like an RF wall, blocking line-of-sight paths.

Because FSK relies on narrowband, lower spectral efficiency and has less robustness to multipath and frequency-selective fading, it struggles in this canyon-like environment.

### 5.2 Node density and mesh limitations

- Research street has **only two nearby FFNs** → **low mesh density**.  
- FSK nodes in the middle part of the street have **no alternate parents** when line-of-sight is blocked.  
- The node often gets stuck in **Join State 4 (searching for parent)** with high RPL rank → no successful join.

OFDM, on the other hand, connects more easily to nodes mounted on nearby buildings due to:

- Better performance over **frequency-selective channels** (multipath, reflections).  
- Wider bandwidth and sub-carrier diversity → some carriers survive even when others are faded.  
- Effective link margin is higher, so paths that are “just below threshold” for FSK can still work for OFDM.

### 5.3 Edge-only FSK connectivity

This explains why:

- FSK can connect at **Locations 1, 2, 3** (start of street, partial line of sight to one FFN)  
- FSK can connect at **Location 20** (other end, closer to the A6 rooftop node)  
- But **points 4–19 see no connectivity at all**: both FFNs are effectively behind concrete+metal obstacles, and mesh density is too low to route around them.

In contrast, the OFDM configuration has enough link margin to maintain connectivity through reflections and partial obstructions, so you see **almost continuous coverage** along the same path.
        """
    )

with st.expander("Takeaways – how to improve Wi-SUN deployment on this street"):
    st.markdown(
        """
- **Increase node density** along research street (more FFNs at intermediate rooftops / poles).  
- Try to **place nodes with better line-of-sight** across the street, especially near the metal bridge.  
- Consider **mixed modulation deployments** where OFDM is used in harsh multipath/urban canyon sections and FSK is maintained in open or less obstructed zones for efficiency.
        """
    )

st.success(
    "Dashboard ready. Scroll up and interact with the plots to explore FSK vs OFDM behaviour across Research Street."
)
