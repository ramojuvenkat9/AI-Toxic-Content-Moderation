import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px

DB_NAME = "moderation.db"

st.set_page_config(
    page_title="Analytics Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Analytics Dashboard")

conn = sqlite3.connect(DB_NAME)

try:
    df = pd.read_sql_query(
        "SELECT * FROM user_history",
        conn
    )
finally:
    conn.close()

if df.empty:

    st.warning("No comments have been analyzed yet.")

else:

    st.header("Overview")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Total Comments",
        len(df)
    )

    col2.metric(
        "Average Toxicity",
        round(df["toxicity"].mean(), 3)
    )

    col3.metric(
        "Average Risk",
        round(df["risk"].mean(), 2)
    )

    if "user_id" in df.columns:
        total_users = df["user_id"].nunique()
    else:
        total_users = 1

    col4.metric(
        "Users",
        total_users
    )

    st.divider()

    st.header("Severity Distribution")

    severity_fig = px.pie(
        df,
        names="severity",
        title="Severity Distribution"
    )

    st.plotly_chart(
        severity_fig,
        use_container_width=True
    )

    st.divider()

    st.header("Risk Score Distribution")

    risk_fig = px.histogram(
        df,
        x="risk",
        nbins=10,
        title="Risk Score Distribution"
    )

    st.plotly_chart(
        risk_fig,
        use_container_width=True
    )

    st.divider()

    st.header("Average Toxicity by Severity")

    toxicity = (
        df.groupby("severity")["toxicity"]
        .mean()
        .reset_index()
    )

    toxicity_fig = px.bar(
        toxicity,
        x="severity",
        y="toxicity",
        title="Average Toxicity"
    )

    st.plotly_chart(
        toxicity_fig,
        use_container_width=True
    )

    st.divider()

    st.header("Recent Comments")

    st.dataframe(
        df.sort_values("id", ascending=False),
        use_container_width=True
    )