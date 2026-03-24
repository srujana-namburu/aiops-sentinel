import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

# DB connection
engine = create_engine("sqlite:///../ingestion-service/aiops.db")

st.set_page_config(page_title="AIOps Dashboard", layout="wide")

st.title("🚀 AIOps Incident Dashboard")

# 🔄 Auto refresh every 5 sec
st.markdown("### 🔄 Auto-refresh enabled (5s)")

@st.cache_data(ttl=5)
def load_data():
    try:
        df = pd.read_sql("SELECT * FROM incidents ORDER BY id DESC", engine)
        return df
    except:
        return pd.DataFrame()

df = load_data()

if df.empty:
    st.warning("No incidents found yet...")
    st.stop()

# 🔍 FILTER SECTION
st.sidebar.header("Filters")

severity_filter = st.sidebar.selectbox(
    "Select Severity",
    ["ALL", "CRITICAL", "HIGH", "MEDIUM", "LOW"]
)

service_filter = st.sidebar.selectbox(
    "Select Service",
    ["ALL"] + list(df["service_name"].unique())
)

# APPLY FILTERS
if severity_filter != "ALL":
    df = df[df["severity"] == severity_filter]

if service_filter != "ALL":
    df = df[df["service_name"] == service_filter]

# 📊 METRICS SECTION
st.subheader("📊 Key Metrics")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Incidents", len(df))
col2.metric("Critical", len(df[df["severity"] == "CRITICAL"]))
col3.metric("High", len(df[df["severity"] == "HIGH"]))
col4.metric("Low", len(df[df["severity"] == "LOW"]))

# 📈 SEVERITY DISTRIBUTION
st.subheader("📈 Severity Distribution")

severity_counts = df["severity"].value_counts()
st.bar_chart(severity_counts)

# 📊 INCIDENT TREND (optional)
if "created_at" in df.columns:
    st.subheader("📅 Incident Trend")
    df["created_at"] = pd.to_datetime(df["created_at"])
    trend = df.groupby(df["created_at"].dt.date).size()
    st.line_chart(trend)

# 📋 INCIDENT TABLE
st.subheader("📋 Incident Details")

st.dataframe(df, use_container_width=True)