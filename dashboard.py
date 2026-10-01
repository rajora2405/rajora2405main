import streamlit as st
import sqlite3
import pandas as pd
import time


# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="Traffic Congestion Monitoring",
    page_icon="🚦",
    layout="wide"
)


# ==========================================
# DATABASE
# ==========================================

DATABASE = "database/traffic.db"


def get_data():

    connection = sqlite3.connect(DATABASE)

    query = """
        SELECT
            id,
            camera_id,
            vehicle_count,
            congestion_level,
            timestamp
        FROM traffic_data
        ORDER BY id DESC
    """

    data = pd.read_sql_query(
        query,
        connection
    )

    connection.close()

    return data


# ==========================================
# HEADER
# ==========================================

st.title("🚦 Intelligent Traffic Congestion Monitoring")

st.markdown(
    "### AI-Based Real-Time Traffic Detection and IoT Monitoring System"
)

st.divider()


# ==========================================
# LOAD DATA
# ==========================================

data = get_data()


if data.empty:

    st.warning("No traffic data available.")

    st.info(
        "Start traffic_iot.py to generate traffic data."
    )

    st.stop()


# ==========================================
# LATEST RECORD
# ==========================================

latest = data.iloc[0]

vehicle_count = int(latest["vehicle_count"])

congestion = latest["congestion_level"]

camera_id = latest["camera_id"]

timestamp = latest["timestamp"]


# ==========================================
# MAIN METRICS
# ==========================================

st.subheader("📊 Current Traffic")

col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "🚗 Vehicles Detected",
        vehicle_count
    )


with col2:

    st.metric(
        "🚦 Congestion",
        congestion
    )


with col3:

    st.metric(
        "📷 Camera",
        camera_id
    )


with col4:

    st.metric(
        "📋 Total Records",
        len(data)
    )


st.divider()


# ==========================================
# CONGESTION STATUS
# ==========================================

st.subheader("Current Congestion Status")


if congestion == "LOW":

    st.success(
        "🟢 LOW — Traffic is moving normally."
    )

elif congestion == "MEDIUM":

    st.warning(
        "🟡 MEDIUM — Moderate traffic congestion detected."
    )

else:

    st.error(
        "🔴 HIGH — Heavy traffic congestion detected."
    )


st.caption(
    f"Last database update: {timestamp}"
)


st.divider()


# ==========================================
# CHARTS
# ==========================================

left, right = st.columns(2)


# ==========================================
# VEHICLE COUNT GRAPH
# ==========================================

with left:

    st.subheader("📈 Vehicle Count Over Time")

    chart_data = data.copy()

    chart_data["timestamp"] = pd.to_datetime(
        chart_data["timestamp"]
    )

    chart_data = chart_data.sort_values(
        "timestamp"
    )

    chart_data = chart_data.set_index(
        "timestamp"
    )

    st.line_chart(
        chart_data["vehicle_count"]
    )


# ==========================================
# CONGESTION DISTRIBUTION
# ==========================================

with right:

    st.subheader("🚦 Congestion Distribution")

    congestion_counts = (
        data["congestion_level"]
        .value_counts()
        .reindex(
            ["LOW", "MEDIUM", "HIGH"],
            fill_value=0
        )
    )

    st.bar_chart(
        congestion_counts
    )


st.divider()


# ==========================================
# TRAFFIC STATISTICS
# ==========================================

st.subheader("📊 Traffic Statistics")


stat1, stat2, stat3, stat4 = st.columns(4)


with stat1:

    st.metric(
        "Average Vehicles",
        f"{data['vehicle_count'].mean():.1f}"
    )


with stat2:

    st.metric(
        "Maximum Vehicles",
        int(data["vehicle_count"].max())
    )


with stat3:

    st.metric(
        "Minimum Vehicles",
        int(data["vehicle_count"].min())
    )


with stat4:

    high_count = (
        data["congestion_level"]
        .eq("HIGH")
        .sum()
    )

    st.metric(
        "High Congestion Events",
        int(high_count)
    )


st.divider()


# ==========================================
# RECENT EVENTS
# ==========================================

st.subheader("📋 Recent Traffic Events")


recent_data = data.head(20).copy()


recent_data.columns = [
    "ID",
    "Camera",
    "Vehicles",
    "Congestion",
    "Timestamp"
]


st.dataframe(
    recent_data,
    width="stretch",
    hide_index=True
)


st.divider()


# ==========================================
# CSV EXPORT
# ==========================================

st.subheader("📥 Export Traffic Data")


csv_data = data.to_csv(
    index=False
).encode("utf-8")


st.download_button(
    label="Download Traffic Data as CSV",
    data=csv_data,
    file_name="traffic_data.csv",
    mime="text/csv"
)


st.divider()


# ==========================================
# SYSTEM INFORMATION
# ==========================================

st.subheader("⚙️ System Information")


info1, info2, info3 = st.columns(3)


with info1:

    st.info(
        "🤖 AI Model\n\nYOLO11n"
    )


with info2:

    st.info(
        "📡 IoT Protocol\n\nMQTT"
    )


with info3:

    st.info(
        "🗄️ Database\n\nSQLite"
    )


# ==========================================
# AUTO REFRESH
# ==========================================

time.sleep(2)

st.rerun()