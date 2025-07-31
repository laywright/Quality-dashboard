# streamlit_app.py

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Jira Issue Dashboard", layout="wide")

st.title("Jira Issue Dashboard")
st.markdown("This dashboard visualizes issue data by type, severity, location, and root cause.")

# Load structured issue data
data = {
    "Chassis Number": [
        "LTPB9G2L4SB000435", "LTPB9G2L6SB000436", "LTPB9G2L5SB000444",
        "LTPB9G2L5SB000444", "LTPB9G2L5SB000444", "LTPB9G2L6SB000436",
        "LTPB9G2L4SB000435", "LTPB9G2L3SB000443", "LTPB9G2L6SB000436",
        "LTPB9G2L4SB000435"
    ],
    "Issue Type": [
        "Supplier Quality", "Production", "Engineering", "Production", "Production",
        "Production", "Engineering", "Warehouse/Inventory", "Production", "Warehouse/Inventory"
    ],
    "Severity": [
        "Low", "Critical", "Low", "Low", "High", "Low", "Medium", "Low", "Low", "Medium"
    ],
    "Issue Found": [
        "Trim", "Quality inspection", "Trim", "EOL", "Trim",
        "Trim", "Trim", "Body", "Body", "Chassis"
    ],
    "Issue Traced To": [
        "Supplier Quality", "Trim", "Engineering", "Body", "OEM",
        "Trim", "OEM", "Warehouse/Inventory", "Body", "Warehouse/Inventory"
    ]
}

df = pd.DataFrame(data)

# Severity color map
severity_colors = {
    "Low": "#0000FF",
    "Medium": "#008000",
    "High": "#F39C12",
    "Critical": "#E74C3C"
}

# Donut Chart: Issue Type
issue_counts = df["Issue Type"].value_counts().reset_index()
issue_counts.columns = ["Issue Type", "Count"]
fig_issue = go.Figure(data=[go.Pie(
    labels=issue_counts["Issue Type"],
    values=issue_counts["Count"],
    hole=0.4
)])
fig_issue.update_layout(title="Issue Type Distribution")

# Pie Chart: Severity
severity_counts = df["Severity"].value_counts().reset_index()
severity_counts.columns = ["Severity", "Count"]
fig_severity = go.Figure(data=[go.Pie(
    labels=severity_counts["Severity"],
    values=severity_counts["Count"],
    marker=dict(colors=[severity_colors.get(s, "#ccc") for s in severity_counts["Severity"]])
)])
fig_severity.update_layout(title="Severity Breakdown")

# Bar Chart: Most Affected Chassis
chassis_counts = df["Chassis Number"].value_counts().reset_index()
chassis_counts.columns = ["Chassis Number", "Issue Count"]
fig_chassis = px.bar(
    chassis_counts,
    x="Chassis Number",
    y="Issue Count",
    color="Issue Count",
    title="Issues per Chassis",
    text_auto=True
)

# Stacked Bar: Severity by Issue Type
severity_order = ["Low", "Medium", "High", "Critical"]
df["Severity"] = pd.Categorical(df["Severity"], categories=severity_order, ordered=True)
fig_sev_type = px.histogram(
    df,
    x="Issue Type",
    color="Severity",
    category_orders={"Severity": severity_order},
    title="Severity Distribution by Issue Type",
    barmode="stack",
    color_discrete_map=severity_colors,
    text_auto=True
)

# Pie Chart: Where Issues Were Found
found_counts = df["Issue Found"].value_counts().reset_index()
found_counts.columns = ["Found In", "Count"]
fig_found = px.pie(
    found_counts,
    names="Found In",
    values="Count",
    title="Where Issues Were Found",
    hole=0.3
)

# Donut Chart: Traced Back Source
traced_counts = df["Issue Traced To"].value_counts().reset_index()
traced_counts.columns = ["Traced To", "Count"]
fig_traced = go.Figure(data=[go.Pie(
    labels=traced_counts["Traced To"],
    values=traced_counts["Count"],
    hole=0.45
)])
fig_traced.update_layout(title="Issue Traced Back To")

# Render charts
st.plotly_chart(fig_issue, use_container_width=True)
st.plotly_chart(fig_severity, use_container_width=True)
st.plotly_chart(fig_chassis, use_container_width=True)
st.plotly_chart(fig_sev_type, use_container_width=True)
st.plotly_chart(fig_found, use_container_width=True)
st.plotly_chart(fig_traced, use_container_width=True)

# Insights
st.subheader("Quick Insights")

# Check for chassis with multiple issues
multi_issues = df["Chassis Number"].value_counts()
high_issue_chassis = multi_issues[multi_issues >= 3]

st.markdown(f"- Chassis with 3 issues:\n{high_issue_chassis.to_string()}")

st.markdown(f"- Most frequent issue type: {df['Issue Type'].value_counts().idxmax()}")
severity_pct = df["Severity"].value_counts(normalize=True).mul(100).round(1).astype(str) + "%"
st.markdown("Severity Distribution (%):")
st.dataframe(severity_pct)
st.markdown(f"- Most common issue location: {df['Issue Found'].value_counts().idxmax()}")
st.markdown(f"- Most common trace-back source: {df['Issue Traced To'].value_counts().idxmax()}")
