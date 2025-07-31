# 📚 Import libraries
import streamlit as st
import pandas as pd
import plotly.express as px

# 🏷 Page configuration
st.set_page_config(page_title="JIRA Quality Issues Dashboard", layout="wide")

# 🚩 Title
st.title("🛠️ Quality Issue Dashboard – JIRA Data")
st.markdown("Upload the JIRA Excel data to explore visual insights from issue tracking.")

# 📤 File uploader
uploaded_file = st.file_uploader("Upload Excel file", type=["xlsx"])

if uploaded_file:
    # 📄 Load data
    df = pd.read_excel(uploaded_file, engine='openpyxl')

    # 🚫 Drop specific chassis numbers
    exclude_chassis = ["LTPB9G2L3SB000426", "LTPB9G2L2SB000434"]
    df = df[~df['Affected Chassis Number'].isin(exclude_chassis)]

    # 🔍 Preview
    st.subheader("📄 Data Preview")
    st.dataframe(df.head())

    st.markdown("---")
    st.subheader("📊 Visual Insights")

    # 🎯 Donut Chart – Issue Type
    issue_type_counts = df['Issue Type'].value_counts().reset_index()
    issue_type_counts.columns = ['Issue Type', 'Count']
    fig_donut = px.pie(issue_type_counts, names='Issue Type', values='Count',
                       title='Issue Type Distribution', hole=0.4)
    st.plotly_chart(fig_donut, use_container_width=True)

    # 🚐 Bar Chart – Chassis Numbers
    chassis_counts = df['Affected Chassis Number'].value_counts().reset_index()
    chassis_counts.columns = ['Chassis Number', 'Count']
    fig_bar = px.bar(chassis_counts.head(10), x='Chassis Number', y='Count',
                     title='Affected Chassis Numbers',
                     labels={'Count': 'Number of Issues'})
    st.plotly_chart(fig_bar, use_container_width=True)

    # ⚠️ Pie Chart – Severity Distribution
    severity_counts = df['Issue Severity'].value_counts().reset_index()
    severity_counts.columns = ['Severity', 'Count']
    fig_severity = px.pie(severity_counts, names='Severity', values='Count',
                          title='Issue Severity Breakdown')
    st.plotly_chart(fig_severity, use_container_width=True)

    # 📊 Stacked Bar – Severity by Issue Type
    severity_by_type = df.groupby(['Issue Type', 'Issue Severity']).size().reset_index(name='Count')
    total_counts = severity_by_type.groupby('Issue Type')['Count'].sum().reset_index()
    sorted_types = total_counts.sort_values(by='Count', ascending=False)['Issue Type']
    severity_by_type['Issue Type'] = pd.Categorical(severity_by_type['Issue Type'],
                                                    categories=sorted_types, ordered=True)

    color_map = {
        'Critical': 'red',
        'High': 'orange',
        'Medium': 'yellow',
        'Low': 'green'
    }

    fig_stacked = px.bar(
        severity_by_type,
        x='Issue Type',
        y='Count',
        color='Issue Severity',
        title='Severity Distribution by Issue Type',
        color_discrete_map=color_map,
        barmode='stack'
    )
    st.plotly_chart(fig_stacked, use_container_width=True)

    # 📈 Insights Summary
    st.markdown("---")
    st.subheader("🔎 Summary Insights")
    st.markdown(f"• **Total issues recorded:** {len(df)}")
    st.markdown(f"• **Most common issue type:** {issue_type_counts.iloc[0]['Issue Type']} ({issue_type_counts.iloc[0]['Count']} cases)")
    st.markdown(f"• **Chassis with most issues:** {chassis_counts.iloc[0]['Chassis Number']} ({chassis_counts.iloc[0]['Count']} issues)")
    st.markdown(f"• **Most frequent severity:** {severity_counts.iloc[0]['Severity']} ({severity_counts.iloc[0]['Count']} issues)")
else:
    st.info("📎 Please upload a valid Excel file to get started.")
