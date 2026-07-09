import io
from pathlib import Path

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

try:
    import pdfplumber

    PDF_SUPPORT = True
except ImportError:
    PDF_SUPPORT = False

# -------------------------------
# PAGE CONFIG
# -------------------------------
st.set_page_config(page_title="Data Analysis Dashboard", layout="wide")

st.title("📊 File Analysis Dashboard")
st.caption("Upload any CSV or PDF (with tables) and get an instant analysis — no fixed schema required.")

# -------------------------------
# DEMO MODE TOGGLE
# -------------------------------
SAMPLE_DATA_PATH = Path(__file__).parent.parent / "data" / "superstore.csv"

st.sidebar.header("🎬 Demo Mode")
demo_mode = st.sidebar.toggle(
    "View demo dataset",
    value=False,
    help="Switch this on to explore the dashboard with the built-in sample Superstore dataset — no upload needed."
)

# -------------------------------
# FILE UPLOAD SECTION
# -------------------------------
st.sidebar.header("📁 Upload Data")
uploaded_file = st.sidebar.file_uploader(
    "Upload a CSV or PDF file",
    type=["csv", "pdf"],
    help="CSV: read directly. PDF: tables are extracted automatically.",
    disabled=demo_mode,
)

if demo_mode:
    st.sidebar.info("Demo mode is ON — using the built-in sample dataset.")
elif uploaded_file is None:
    st.info("👈 Turn on **Demo Mode** or upload a CSV/PDF file in the sidebar to get started.")
    st.stop()


# -------------------------------
# HELPERS
# -------------------------------
@st.cache_data(show_spinner=False)
def extract_pdf_tables(file_bytes):
    """Extract all tables found in a PDF, returns list of dicts with page, index, df."""
    results = []
    with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
        for page_num, page in enumerate(pdf.pages, start=1):
            page_tables = page.extract_tables()
            for t_idx, table in enumerate(page_tables, start=1):
                if table and len(table) > 1:
                    header, *rows = table
                    header = [str(h).strip() if h else f"col_{i}" for i, h in enumerate(header)]
                    df = pd.DataFrame(rows, columns=header)
                    results.append({"page": page_num, "index": t_idx, "df": df})
    return results


def coerce_types(df):
    """Try to convert object columns to numeric or datetime where it makes sense."""
    df = df.copy()
    df.columns = [str(c).strip().replace(" ", "_") for c in df.columns]

    for col in df.columns:
        if df[col].dtype == object:
            # try numeric first
            cleaned = (
                df[col]
                .astype(str)
                .str.replace(",", "", regex=False)
                .str.replace("$", "", regex=False)
                .str.replace("%", "", regex=False)
                .str.strip()
            )
            numeric = pd.to_numeric(cleaned, errors="coerce")
            if numeric.notna().mean() > 0.8:
                df[col] = numeric
                continue

            # try datetime
            parsed = pd.to_datetime(df[col], errors="coerce")
            if parsed.notna().mean() > 0.8:
                df[col] = parsed
                continue

    return df


def load_csv(file):
    df = pd.read_csv(file)
    return coerce_types(df)


@st.cache_data(show_spinner=False)
def load_sample_data():
    if not SAMPLE_DATA_PATH.exists():
        return None
    df = pd.read_csv(SAMPLE_DATA_PATH)
    return coerce_types(df)


# -------------------------------
# LOAD DATA
# -------------------------------
df = None

if demo_mode:
    df = load_sample_data()
    if df is None:
        st.error(
            f"❌ Demo dataset not found at `{SAMPLE_DATA_PATH}`.\n\n"
            "Make sure 'superstore.csv' is inside the project's 'data/' folder, "
            "or turn off Demo Mode and upload your own file."
        )
        st.stop()
    st.sidebar.success(f"✅ Demo dataset loaded ({len(df):,} rows, {len(df.columns)} cols)")

else:
    file_bytes = uploaded_file.getvalue()
    file_name = uploaded_file.name.lower()

    if file_name.endswith(".csv"):
        try:
            df = load_csv(io.BytesIO(file_bytes))
            st.sidebar.success(f"✅ Loaded '{uploaded_file.name}' ({len(df):,} rows, {len(df.columns)} cols)")
        except Exception as e:
            st.error(f"❌ Could not read this CSV. Error: {e}")
            st.stop()

    elif file_name.endswith(".pdf"):
        if not PDF_SUPPORT:
            st.error("❌ PDF support requires the 'pdfplumber' package. Add it to requirements.txt and reinstall.")
            st.stop()

        with st.spinner("Extracting tables from PDF..."):
            tables = extract_pdf_tables(file_bytes)

        if not tables:
            st.warning("⚠️ No tables were found in this PDF. Only PDFs containing tabular data can be analyzed.")
            st.stop()

        if len(tables) == 1:
            chosen = tables[0]
        else:
            labels = [f"Page {t['page']}, Table {t['index']} ({len(t['df'])} rows)" for t in tables]
            choice = st.sidebar.selectbox("Multiple tables found — choose one to analyze", labels)
            chosen = tables[labels.index(choice)]

        df = coerce_types(chosen["df"])
        st.sidebar.success(f"✅ Loaded table from page {chosen['page']} ({len(df):,} rows, {len(df.columns)} cols)")

if df is None or df.empty:
    st.warning("⚠️ No usable data found in this file.")
    st.stop()

# -------------------------------
# DETECT COLUMN TYPES
# -------------------------------
numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
date_cols = df.select_dtypes(include=["datetime64[ns]"]).columns.tolist()
categorical_cols = [c for c in df.columns if c not in numeric_cols and c not in date_cols]

# -------------------------------
# SIDEBAR FILTERS
# -------------------------------
st.sidebar.header("Filter Data")
filtered_df = df.copy()

# Categorical filters (limit to reasonably low-cardinality columns)
filterable_cats = [c for c in categorical_cols if df[c].nunique(dropna=True) <= 50]
for col in filterable_cats[:5]:
    options = df[col].dropna().unique().tolist()
    selected = st.sidebar.multiselect(f"{col}", options=options, default=options)
    if selected:
        filtered_df = filtered_df[filtered_df[col].isin(selected)]

# Date filter (first date column only)
if date_cols:
    date_col = date_cols[0]
    min_date, max_date = df[date_col].min(), df[date_col].max()
    if pd.notna(min_date) and pd.notna(max_date):
        date_range = st.sidebar.date_input(
            f"Filter by {date_col}",
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date,
        )
        if isinstance(date_range, tuple) and len(date_range) == 2:
            start_date, end_date = date_range
            filtered_df = filtered_df[
                (filtered_df[date_col] >= pd.to_datetime(start_date)) &
                (filtered_df[date_col] <= pd.to_datetime(end_date))
                ]

if filtered_df.empty:
    st.warning("⚠️ No data matches the selected filters. Please adjust them.")
    st.stop()

# -------------------------------
# OVERVIEW METRICS
# -------------------------------
st.subheader("Overview")
c1, c2, c3, c4 = st.columns(4)
c1.metric("Rows", f"{len(filtered_df):,}")
c2.metric("Columns", f"{len(filtered_df.columns):,}")
missing_pct = filtered_df.isna().mean().mean() * 100
c3.metric("Missing Data", f"{missing_pct:.1f}%")
c4.metric("Numeric Columns", f"{len(numeric_cols)}")

# -------------------------------
# KPI ON A CHOSEN NUMERIC COLUMN
# -------------------------------
if numeric_cols:
    st.subheader("💰 Key Metric Summary")
    metric_col = st.selectbox("Choose a numeric column to summarize", numeric_cols)
    k1, k2, k3, k4 = st.columns(4)
    series = filtered_df[metric_col].dropna()
    k1.metric(f"Sum of {metric_col}", f"{series.sum():,.2f}")
    k2.metric(f"Average {metric_col}", f"{series.mean():,.2f}")
    k3.metric(f"Max {metric_col}", f"{series.max():,.2f}")
    k4.metric(f"Min {metric_col}", f"{series.min():,.2f}")

# -------------------------------
# AUTO INSIGHTS
# -------------------------------
st.subheader("💡 Key Insights")
insights = []

if numeric_cols:
    for col in numeric_cols:
        s = filtered_df[col].dropna()
        if len(s) == 0:
            continue
        q1, q3 = s.quantile(0.25), s.quantile(0.75)
        iqr = q3 - q1
        outliers = s[(s < q1 - 1.5 * iqr) | (s > q3 + 1.5 * iqr)]
        if len(outliers) > 0:
            insights.append(f"- **⚠️ {col}**: {len(outliers)} potential outlier(s) detected.")

missing_by_col = filtered_df.isna().mean().sort_values(ascending=False)
top_missing = missing_by_col[missing_by_col > 0].head(3)
if not top_missing.empty:
    for col, pct in top_missing.items():
        insights.append(f"- **🕳️ {col}**: {pct * 100:.1f}% missing values.")

if len(numeric_cols) >= 2:
    corr = filtered_df[numeric_cols].corr(numeric_only=True).abs()

    # ---------------------------------------------------------
    # BUG FIX: Create writable copy to prevent read-only error
    # ---------------------------------------------------------
    corr_array = corr.to_numpy(copy=True)
    np.fill_diagonal(corr_array, 0)
    corr.iloc[:, :] = corr_array

    if corr.size > 0:
        max_pair = corr.stack().idxmax()
        max_val = corr.stack().max()
        if max_val > 0.6:
            insights.append(f"- **🔗 Strong correlation**: {max_pair[0]} and {max_pair[1]} (r={max_val:.2f}).")

if categorical_cols:
    col = categorical_cols[0]
    top_val = filtered_df[col].mode()
    if not top_val.empty:
        insights.append(f"- **🏆 Most common {col}**: {top_val.iloc[0]}.")

if not insights:
    insights.append("- No notable issues or patterns detected in this dataset.")

st.info("\n".join(insights))

# -------------------------------
# DATA PREVIEW + DOWNLOAD
# -------------------------------
st.subheader("Data Preview")
st.dataframe(filtered_df.head(50), width='stretch')

csv_data = filtered_df.to_csv(index=False)
st.download_button(
    "📥 Download filtered data as CSV",
    data=csv_data,
    file_name="filtered_data.csv",
    mime="text/csv",
)

# -------------------------------
# CHARTS
# -------------------------------
if categorical_cols:
    st.subheader("Category Breakdown")
    cat_col = st.selectbox("Choose a categorical column", categorical_cols, key="cat_chart")
    if numeric_cols:
        val_col = st.selectbox("Aggregate by numeric column", numeric_cols, key="cat_val")
        agg_df = (
            filtered_df.groupby(cat_col)[val_col]
            .sum()
            .sort_values(ascending=False)
            .head(20)
            .reset_index()
        )
        fig_cat = px.bar(agg_df, x=cat_col, y=val_col, title=f"{val_col} by {cat_col} (Top 20)")
    else:
        agg_df = filtered_df[cat_col].value_counts().head(20).reset_index()
        agg_df.columns = [cat_col, "count"]
        fig_cat = px.bar(agg_df, x=cat_col, y="count", title=f"Count of {cat_col} (Top 20)")
    st.plotly_chart(fig_cat, width='stretch')

if numeric_cols:
    st.subheader("Distribution")
    dist_col = st.selectbox("Choose a numeric column", numeric_cols, key="dist_chart")
    fig_hist = px.histogram(filtered_df, x=dist_col, title=f"Distribution of {dist_col}")
    st.plotly_chart(fig_hist, width='stretch')

if len(numeric_cols) >= 2:
    st.subheader("Correlation")
    corr_matrix = filtered_df[numeric_cols].corr(numeric_only=True)
    fig_corr = px.imshow(
        corr_matrix,
        text_auto=".2f",
        color_continuous_scale="RdBu_r",
        title="Correlation Heatmap",
        zmin=-1,
        zmax=1,
    )
    st.plotly_chart(fig_corr, width='stretch')

    st.subheader("Scatter Plot")
    sc1, sc2 = st.columns(2)
    x_col = sc1.selectbox("X axis", numeric_cols, index=0, key="scatter_x")
    y_col = sc2.selectbox("Y axis", numeric_cols, index=min(1, len(numeric_cols) - 1), key="scatter_y")
    fig_scatter = px.scatter(filtered_df, x=x_col, y=y_col, title=f"{y_col} vs {x_col}")
    st.plotly_chart(fig_scatter, width='stretch')

if date_cols and numeric_cols:
    st.subheader("📅 Trend Over Time")
    trend_date_col = date_cols[0]
    trend_val_col = st.selectbox("Value to trend", numeric_cols, key="trend_val")
    trend_df = filtered_df.dropna(subset=[trend_date_col]).copy()
    trend_df = trend_df.set_index(trend_date_col).resample("ME")[trend_val_col].sum().reset_index()
    fig_trend = px.line(
        trend_df, x=trend_date_col, y=trend_val_col,
        title=f"{trend_val_col} Over Time (Monthly)", markers=True
    )
    st.plotly_chart(fig_trend, width='stretch')