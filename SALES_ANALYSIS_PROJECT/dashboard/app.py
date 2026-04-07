import streamlit as st
import pandas as pd
import plotly.express as px
import os

# -------------------------------
# PAGE CONFIG
# -------------------------------
st.set_page_config(page_title="Sales Dashboard", layout="wide")

# -------------------------------
# TITLE
# -------------------------------
st.title("📊 Sales & Revenue Dashboard")

# -------------------------------
# LOAD DATA
# -------------------------------
data_path = os.path.join(os.path.dirname(__file__), '../data/superstore.csv')
df = pd.read_csv(data_path)

# clean columns
df.columns = df.columns.str.strip().str.replace(' ', '_')

# -------------------------------
# SIDEBAR FILTERS
# -------------------------------
st.sidebar.header("Filter Data")

region = st.sidebar.multiselect(
    "Select Region",
    options=df['Region'].unique(),
    default=df['Region'].unique()
)

category = st.sidebar.multiselect(
    "Select Category",
    options=df['Category'].unique(),
    default=df['Category'].unique()
)

# apply filters
filtered_df = df[
    (df['Region'].isin(region)) &
    (df['Category'].isin(category))
]

# -------------------------------
# KPI METRICS
# -------------------------------
st.subheader("Key Metrics")

col1, col2, col3 = st.columns(3)

col1.metric("Total Sales", f"{filtered_df['Sales'].sum():,.2f}")
col2.metric("Total Profit", f"{filtered_df['Profit'].sum():,.2f}")
col3.metric("Total Quantity", int(filtered_df['Quantity'].sum()))

# -------------------------------
# DATA PREVIEW
# -------------------------------
st.subheader("Data Preview")
st.write(filtered_df.head())

# -------------------------------
# CHART 1: SALES BY REGION
# -------------------------------
st.subheader("Sales by Region")

region_sales = filtered_df.groupby('Region')['Sales'].sum().reset_index()

fig1 = px.bar(region_sales, x='Region', y='Sales', title="Sales by Region")
st.plotly_chart(fig1, use_container_width=True)

# -------------------------------
# CHART 2: SALES BY CATEGORY
# -------------------------------
st.subheader("Sales by Category")

category_sales = filtered_df.groupby('Category')['Sales'].sum().reset_index()

fig2 = px.bar(category_sales, x='Category', y='Sales', title="Sales by Category")
st.plotly_chart(fig2, use_container_width=True)

# -------------------------------
# CHART 3: TOP 10 CITIES
# -------------------------------
st.subheader("Top 10 Cities by Sales")

top_cities = filtered_df.groupby('City')['Sales'].sum().nlargest(10).reset_index()

fig3 = px.bar(top_cities, x='City', y='Sales', title="Top Cities")
st.plotly_chart(fig3, use_container_width=True)


