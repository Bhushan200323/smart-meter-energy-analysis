import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(page_title="Smart Energy Dashboard",
                   page_icon="⚡",
                   layout="wide")

st.title("⚡ Smart Meter Energy Analysis Dashboard")
st.markdown("Advanced Interactive Energy Monitoring System")

# -----------------------------
# Load CSV File
# -----------------------------
df = pd.read_csv("smart_meter_data.csv")

# -----------------------------
# Data Cleaning
# -----------------------------
df.dropna(inplace=True)
df.drop_duplicates(inplace=True)

df['Timestamp'] = pd.to_datetime(df['Timestamp'])
df['Hour'] = df['Timestamp'].dt.hour
df['Month'] = df['Timestamp'].dt.month

df['Anomaly_Label'] = df['Anomaly_Label'].map({
    'Normal': 0,
    'Abnormal': 1
})

# -----------------------------
# Sidebar Filters
# -----------------------------
st.sidebar.header("🔍 Filter Data")

selected_month = st.sidebar.multiselect(
    "Select Month",
    options=df['Month'].unique(),
    default=df['Month'].unique()
)

df = df[df['Month'].isin(selected_month)]

# -----------------------------
# KPI Section
# -----------------------------
col1, col2, col3 = st.columns(3)

col1.metric("Total Consumption",
            f"{df['Electricity_Consumed'].sum():.2f}")

col2.metric("Average Consumption",
            f"{df['Electricity_Consumed'].mean():.2f}")

col3.metric("Total Anomalies",
            df[df['Anomaly_Label']==1].shape[0])

st.divider()

# -----------------------------
# Tabs
# -----------------------------
tab1, tab2, tab3, tab4 = st.tabs([
    "📈 Time Analysis",
    "🌡 Environmental Impact",
    "⚠️ Anomaly Detection",
    "📊 Advanced Analytics"
])

# =============================
# TAB 1 – TIME ANALYSIS
# =============================
with tab1:

    hourly = df.groupby('Hour')['Electricity_Consumed'].mean().reset_index()

    fig1 = px.bar(hourly, x='Hour', y='Electricity_Consumed',
                  title="Hourly Consumption Trend")
    st.plotly_chart(fig1, use_container_width=True)

    monthly = df.groupby('Month')['Electricity_Consumed'].mean().reset_index()

    fig2 = px.line(monthly, x='Month',
                   y='Electricity_Consumed',
                   markers=True,
                   title="Monthly Consumption Trend")
    st.plotly_chart(fig2, use_container_width=True)

# =============================
# TAB 2 – ENVIRONMENTAL IMPACT
# =============================
with tab2:

    fig3 = px.scatter(df,
                      x='Temperature',
                      y='Electricity_Consumed',
                      color='Anomaly_Label',
                      title="Temperature vs Consumption")
    st.plotly_chart(fig3, use_container_width=True)

    df['Humidity_Level'] = pd.cut(df['Humidity'],
                                  bins=[0,30,60,100],
                                  labels=['Low','Medium','High'])

    humidity_data = df.groupby('Humidity_Level')['Electricity_Consumed'].mean().reset_index()

    fig4 = px.bar(humidity_data,
                  x='Humidity_Level',
                  y='Electricity_Consumed',
                  title="Humidity Level vs Consumption")
    st.plotly_chart(fig4, use_container_width=True)

# =============================
# TAB 3 – ANOMALY DETECTION
# =============================
with tab3:

    anomaly_counts = df['Anomaly_Label'].value_counts().reset_index()
    anomaly_counts.columns = ['Anomaly_Label', 'Count']

    fig5 = px.pie(anomaly_counts,
                  values='Count',
                  names='Anomaly_Label',
                  hole=0.4,
                  title="Anomaly Distribution")
    st.plotly_chart(fig5, use_container_width=True)

    fig6 = px.box(df,
                  x='Anomaly_Label',
                  y='Electricity_Consumed',
                  title="Normal vs Abnormal Consumption")
    st.plotly_chart(fig6, use_container_width=True)

# =============================
# TAB 4 – ADVANCED ANALYTICS
# =============================
with tab4:

    # 1️⃣ Distribution Histogram
    fig7 = px.histogram(df,
                        x='Electricity_Consumed',
                        nbins=30,
                        title="Distribution of Electricity Consumption")
    st.plotly_chart(fig7, use_container_width=True)

    # 2️⃣ Boxplot for Outliers
    fig8 = px.box(df,
                  y='Electricity_Consumed',
                  title="Outlier Detection (Box Plot)")
    st.plotly_chart(fig8, use_container_width=True)

    # 3️⃣ Correlation Heatmap
    st.subheader("Correlation Heatmap")

    corr = df.corr(numeric_only=True)

    fig9 = px.imshow(corr,
                     text_auto=True,
                     color_continuous_scale='RdBu_r')
    st.plotly_chart(fig9, use_container_width=True)

    # 4️⃣ Hour vs Month Heatmap
    pivot = df.pivot_table(values='Electricity_Consumed',
                           index='Hour',
                           columns='Month',
                           aggfunc='mean')

    fig10 = px.imshow(pivot,
                      title="Hour vs Month Heatmap",
                      color_continuous_scale='Viridis')
    st.plotly_chart(fig10, use_container_width=True)

    # 5️⃣ Past vs Current Consumption
    fig11 = px.scatter(df,
                       x='Avg_Past_Consumption',
                       y='Electricity_Consumed',
                       title="Past vs Current Consumption")
    st.plotly_chart(fig11, use_container_width=True)
