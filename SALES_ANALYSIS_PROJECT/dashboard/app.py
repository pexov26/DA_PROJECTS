import subprocess, sys
subprocess.run([sys.executable, "-m", "pip", "install", "plotly", "pandas", "streamlit"])
import streamlit as st
import pandas as pd
from pathlib import Path

# Try to import plotly, show friendly error if missing
try:
    import plotly.express as px
except ImportError as e:
    st.error(f"Plotly not installed. Error: {e}")
    st.stop()
# -------------------------------
# PAGE CONFIG
# -------------------------------
st.set_page_config(page_title="Sales Dashboard", layout="wide")

# -------------------------------
# TITLE
# -------------------------------
st.title("📊 Sales & Revenue Dashboard")

# -------------------------------
# LOAD DATA (with caching & error handling)
# -------------------------------
@st.cache_data
def load_data():
    data_path = Path(__file__).parent.parent / "data" / "superstore.csv"
    if not data_path.exists():
        st.error(f"❌ Data file not found at {data_path}\nPlease make sure 'superstore.csv' is inside the 'data/' folder.")
        st.stop()
    df = pd.read_csv(data_path)
    df.columns = df.columns.str.strip().str.replace(' ', '_')
    if 'Order_Date' in df.columns:
        df['Order_Date'] = pd.to_datetime(df['Order_Date'])
    if 'Ship_Date' in df.columns:
        df['Ship_Date'] = pd.to_datetime(df['Ship_Date'])
    return df

df = load_data()   # IMPORTANT: call the function

# -------------------------------
# VALIDATE REQUIRED COLUMNS
# -------------------------------
required_columns = ['Sales', 'Profit', 'Quantity', 'Region', 'Category', 'City']
missing_cols = [col for col in required_columns if col not in df.columns]
if missing_cols:
    st.error(f"❌ Missing required columns: {missing_cols}\nPlease check your CSV file.")
    st.stop()

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

if 'Order_Date' in df.columns:
    st.sidebar.subheader("Filter by Date")
    min_date = df['Order_Date'].min()
    max_date = df['Order_Date'].max()
    date_range = st.sidebar.date_input(
        "Select date range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )
else:
    date_range = None
    # st.sidebar.info("Order_Date column not found. Date filtering disabled.")   # commented out

# -------------------------------
# APPLY FILTERS
# -------------------------------
filtered_df = df[
    (df['Region'].isin(region)) &
    (df['Category'].isin(category))
]

if 'Order_Date' in df.columns and date_range and len(date_range) == 2:
    start_date, end_date = date_range
    filtered_df = filtered_df[
        (filtered_df['Order_Date'] >= pd.to_datetime(start_date)) &
        (filtered_df['Order_Date'] <= pd.to_datetime(end_date))
    ]

# -------------------------------
# CHECK FOR EMPTY FILTERED DATA
# -------------------------------
if filtered_df.empty:
    st.warning("⚠️ No data matches the selected filters. Please adjust Region, Category, or Date range.")
    st.stop()

# -------------------------------
# KPI METRICS (4 columns with profit margin)
# -------------------------------
st.subheader("Key Metrics")

col1, col2, col3, col4 = st.columns(4)

total_sales = filtered_df['Sales'].sum()
total_profit = filtered_df['Profit'].sum()
total_quantity = int(filtered_df['Quantity'].sum())
profit_margin = (total_profit / total_sales * 100) if total_sales > 0 else 0

col1.metric("Total Sales", f"${total_sales:,.2f}")
col2.metric("Total Profit", f"${total_profit:,.2f}")
col3.metric("Total Quantity", f"{total_quantity:,}")
col4.metric("Profit Margin", f"{profit_margin:.1f}%")

# -------------------------------
# AUTO-GENERATED INSIGHTS
# -------------------------------
st.subheader("💡 Key Insights")

# Calculate top region
region_sales = filtered_df.groupby('Region')['Sales'].sum().reset_index()
top_region = region_sales.loc[region_sales['Sales'].idxmax()]
top_region_name = top_region['Region']
top_region_sales = top_region['Sales']

# Calculate top category
cat_sales = filtered_df.groupby('Category')['Sales'].sum().reset_index()
top_cat = cat_sales.loc[cat_sales['Sales'].idxmax()]
top_cat_name = top_cat['Category']
top_cat_sales = top_cat['Sales']

# Calculate profit margin (already have from KPIs, but recompute for safety)
margin = (filtered_df['Profit'].sum() / filtered_df['Sales'].sum() * 100) if filtered_df['Sales'].sum() > 0 else 0

# Find loss-making sub-categories
sub_cat_col = None
for col in filtered_df.columns:
    if 'sub' in col.lower() and 'category' in col.lower():
        sub_cat_col = col
        break

loss_count = 0
loss_names = []
if sub_cat_col:
    subcat_profit = filtered_df.groupby(sub_cat_col)['Profit'].sum()
    loss_makers = subcat_profit[subcat_profit < 0]
    loss_count = len(loss_makers)
    loss_names = loss_makers.index.tolist()

# Build insight text
insights = f"""
- **🏆 Top Region**: {top_region_name} with **${top_region_sales:,.0f}** in sales.
- **📦 Top Category**: {top_cat_name} with **${top_cat_sales:,.0f}** in sales.
- **📊 Profit Margin**: {margin:.1f}% 
"""

# Add warning if margin is low
if margin < 10:
    insights += "  ⚠️ *Margin is below 10% – consider reviewing discounts or costs.*\n"
else:
    insights += "  ✅ *Healthy margin.*\n"

# Add loss-making sub-categories info
if loss_count > 0:
    loss_list = ", ".join(loss_names[:3])  # show first 3 only
    if loss_count > 3:
        loss_list += f" and {loss_count - 3} more"
    insights += f"- **⚠️ Loss-making sub‑categories**: {loss_count} found ({loss_list}).\n"
else:
    insights += "- **✅ Profitability**: All sub‑categories are profitable.\n"

# Display insights in an info box
st.info(insights)

# -------------------------------
# DATA PREVIEW
# -------------------------------
st.subheader("Data Preview")
st.write(filtered_df.head())

# Download button
csv_data = filtered_df.to_csv(index=False)
st.download_button(
    label="📥 Download filtered data as CSV",
    data=csv_data,
    file_name="filtered_sales_data.csv",
    mime="text/csv"
)

# -------------------------------
# CHART 1: SALES BY REGION (sorted)
# -------------------------------
st.subheader("Sales by Region")
region_sales = filtered_df.groupby('Region')['Sales'].sum().sort_values(ascending=False).reset_index()
fig1 = px.bar(region_sales, x='Region', y='Sales', title="Sales by Region (Highest First)")
st.plotly_chart(fig1, width='stretch')   # replaced use_container_width

# -------------------------------
# CHART 2: SALES BY CATEGORY (sorted)
# -------------------------------
st.subheader("Sales by Category")
category_sales = filtered_df.groupby('Category')['Sales'].sum().sort_values(ascending=False).reset_index()
fig2 = px.bar(category_sales, x='Category', y='Sales', title="Sales by Category (Highest First)")
st.plotly_chart(fig2, width='stretch')

# -------------------------------
# CHART 3: TOP N CITIES (dynamic slider)
# -------------------------------
st.subheader("Top Cities by Sales")
n_cities = st.slider("Number of top cities to display", min_value=5, max_value=20, value=10, step=1)
top_cities = filtered_df.groupby('City')['Sales'].sum().nlargest(n_cities).reset_index()
fig3 = px.bar(top_cities, x='City', y='Sales', title=f"Top {n_cities} Cities by Sales")
st.plotly_chart(fig3, width='stretch')

# -------------------------------
# CHART 4: Scatter Plot (Sales vs Profit by Sub-Category)
# -------------------------------
st.subheader("Profitability by Sub‑Category")

# Find sub-category column
sub_cat_col = None
for col in filtered_df.columns:
    if 'sub' in col.lower() and 'category' in col.lower():
        sub_cat_col = col
        break

if sub_cat_col:
    subcat_data = filtered_df.groupby(sub_cat_col)[['Sales', 'Profit']].sum().reset_index()
    fig_scatter = px.scatter(
        subcat_data,
        x='Sales',
        y='Profit',
        text=sub_cat_col,
        title="Sales vs Profit by Sub‑Category (Size = Sales, Color = Profit)",
        color='Profit',
        color_continuous_scale='RdYlGn',
        size='Sales',
        size_max=60,
        hover_name=sub_cat_col
    )
    fig_scatter.update_traces(textposition='top center')
    fig_scatter.add_hline(y=0, line_dash="dash", line_color="gray", opacity=0.5)
    st.plotly_chart(fig_scatter, width='stretch')
    
    loss_makers = subcat_data[subcat_data['Profit'] < 0]
    if not loss_makers.empty:
        st.warning(f"⚠️ {len(loss_makers)} sub‑category(s) are operating at a loss: {', '.join(loss_makers[sub_cat_col].astype(str))}")
else:
    st.info("ℹ️ Sub‑Category column not found. Cannot create scatter plot.")

    # -------------------------------
# CHART 5: Monthly Sales Trend (if Order_Date exists)
# -------------------------------
st.subheader("📅 Monthly Sales Trend")

if 'Order_Date' in filtered_df.columns:
    # Create a copy and set date as index for resampling
    trend_df = filtered_df.copy()
    trend_df.set_index('Order_Date', inplace=True)
    
    # Resample by month and sum sales
    monthly_sales = trend_df.resample('M')['Sales'].sum().reset_index()
    
    # Create line chart with markers
    fig_line = px.line(
        monthly_sales,
        x='Order_Date',
        y='Sales',
        title="Total Sales per Month",
        markers=True,
        line_shape='linear'
    )
    
    # Improve formatting
    fig_line.update_layout(
        xaxis_title="Month",
        yaxis_title="Total Sales ($)",
        hovermode='x unified'
    )
    
    st.plotly_chart(fig_line, width='stretch')
else:
    st.info("ℹ️ Monthly trend chart requires an 'Order_Date' column. Add it to your CSV to enable this feature.")