import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import altair as alt

# Streamlit Setup
st.set_page_config(page_title="Customer Operations Dashboard", layout="wide")

st.markdown("""
    <style>
    h1 {
        font-size: 2.5rem;
        font-weight: 700;
        color: #FFFFFF;
    }
    .block-container {
        padding-top: 2rem;
    }
    .stMetric {
        background-color: #1e1e1e;
        border-radius: 10px;
        padding: 20px;
    }
    </style>
""", unsafe_allow_html=True)

st.title("📊 Customer Operations Intelligence")

# DB connection
engine = create_engine("mysql+mysqlconnector://root:root@localhost/customer_ops_simulator")

@st.cache_data
def load_data():
    rules = pd.read_sql("SELECT * FROM rules", engine)
    logs = pd.read_sql("SELECT * FROM execution_logs", engine)
    tickets = pd.read_sql("SELECT * FROM tickets", engine)
    customers = pd.read_sql("SELECT * FROM customers", engine)
    return rules, logs, tickets, customers

rules, logs, tickets, customers = load_data()

# KPIs
st.markdown("### 📈 Key Metrics")
col1, col2, col3, col4 = st.columns(4)
col1.metric("👥 Customers", customers.shape[0])
col2.metric("⚙️ Rules", rules.shape[0])
col3.metric("📄 Executions", logs.shape[0])
col4.metric("❌ Tickets Open", tickets[tickets["status"] == "open"].shape[0])

st.markdown("---")

# === Sidebar Filters ===
st.sidebar.header("🔍 Filters")
status_filter = st.sidebar.selectbox("Rule Execution Status", ["All", "success", "failure"])
priority_filter = st.sidebar.selectbox("Customer Priority", ["All"] + customers["priority_level"].unique().tolist())
customer_name_input = st.sidebar.text_input("Search Customer Name")

# === Filter Logs ===
filtered_logs = logs.copy()

if status_filter != "All":
    filtered_logs = filtered_logs[filtered_logs["status"] == status_filter]

if priority_filter != "All":
    priority_ids = customers[customers["priority_level"] == priority_filter]["id"]
    filtered_logs = filtered_logs[filtered_logs["customer_id"].isin(priority_ids)]

if customer_name_input:
    matched_ids = customers[customers["name"].str.contains(customer_name_input, case=False)]["id"]
    filtered_logs = filtered_logs[filtered_logs["customer_id"].isin(matched_ids)]

# === Join with Customer Info ===
filtered_logs = pd.merge(filtered_logs, customers[["id", "name"]], left_on="customer_id", right_on="id")

# === Execution Trend ===
st.markdown("### 📆 Rule Executions Over Time")
logs["executed_date"] = pd.to_datetime(logs["executed_at"]).dt.date
daily_logs = logs.groupby("executed_date").size().reset_index(name="count")
st.area_chart(daily_logs.set_index("executed_date"))

# === Summary Data Preparation ===
st.markdown("### ✅ Execution Success/Failure per Customer")

summary = (
    filtered_logs.groupby(["name", "status"]).size()
    .unstack()
    .fillna(0)
    .reset_index()
    .rename(columns={"name": "Customer"})
)

# Ensure both columns exist
if "success" not in summary.columns:
    summary["success"] = 0
if "failure" not in summary.columns:
    summary["failure"] = 0

summary["Total"] = summary["success"] + summary["failure"]
summary = summary[summary["Total"] > 0]
summary["Success Rate"] = (summary["success"] / summary["Total"]).round(2)

# === Final Stacked Bar Chart ===
chart_df = summary.melt(
    id_vars=["Customer"],
    value_vars=["success", "failure"],
    var_name="Status",
    value_name="Count"
)

if summary.empty:
    st.warning("⚠️ No execution data found for the current filter settings.")
else:
    bar_chart = (
        alt.Chart(chart_df)
        .mark_bar(size=18)
        .encode(
            x=alt.X(
    "Customer:N",
    sort="-y",
    title="Customer",
    axis=alt.Axis(
        # labelAngle=-45,
        labelFontSize=12,
        labelLimit=100,
        labelOverlap="parity"
    )
),


            y=alt.Y("Count:Q", title="Executions"),
            color=alt.Color("Status:N", scale=alt.Scale(
                domain=["success", "failure"],
                range=["#2ECC71", "#E74C3C"]
            )),
            tooltip=["Customer", "Status", "Count"]
        )
        .properties(
            height=450,
            width="container",
            title=alt.TitleParams(
                text="Execution Success/Failure per Customer",
                fontSize=18,
                anchor="start",
                fontWeight="bold"
            )
        )
        .configure_axis(
            labelFontSize=12,
            titleFontSize=14
        )
        .configure_legend(
            orient="top-right",
            title=None,
            labelFontSize=12
        )
        .interactive()
    )

    st.altair_chart(bar_chart, use_container_width=True)

# === CSV Export ===
st.download_button(
    label="📥 Download Filtered Logs (CSV)",
    data=filtered_logs.to_csv(index=False).encode('utf-8'),
    file_name="filtered_execution_logs.csv",
    mime="text/csv"
)

# === Tables ===
with st.expander("📊 Summary Table"):
    st.dataframe(summary[["Customer", "success", "failure", "Success Rate"]], use_container_width=True)

with st.expander("📋 Raw Execution Logs"):
    st.dataframe(filtered_logs[["name", "rule_id", "status", "executed_at"]].sort_values(by="executed_at", ascending=False), use_container_width=True)
