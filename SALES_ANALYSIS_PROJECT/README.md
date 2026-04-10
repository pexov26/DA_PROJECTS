# 📊 Sales & Revenue Analysis Dashboard

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://daprojects-rc8u8u8hzdlmaec2bsl9zu.streamlit.app/)

**Live Demo:** [Click here to view the dashboard](https://daprojects-rc8u8u8hzdlmaec2bsl9zu.streamlit.app/)

---

## 🚀 Project Overview

This project is an **interactive sales dashboard** built with Python and Streamlit. It transforms raw retail data into actionable business insights, allowing users to explore sales performance across regions, categories, cities, and time periods.

The dashboard is deployed on **Streamlit Cloud** and can be accessed by anyone – no installation required.

---

## 📌 Key Features

| Feature | Description |
|---------|-------------|
| **Dynamic Filters** | Filter by Region, Category, and Date (if available) |
| **KPI Metrics** | Total Sales, Total Profit, Quantity, and Profit Margin |
| **Auto‑generated Insights** | Highlights top region, category, and loss‑making sub‑categories |
| **Interactive Charts** | Bar charts (sorted), scatter plot for profitability, and top N cities slider |
| **Data Export** | Download filtered data as CSV with one click |
| **Responsive UI** | Clean layout with full‑width charts |

---

## 🛠️ Tech Stack

- **Python** – Core logic and data processing
- **Pandas** – Data manipulation and aggregation
- **Plotly** – Interactive visualizations
- **Streamlit** – Dashboard framework and deployment

---

## 📈 Business Insights Gained

- **Regional performance** – West region generates the highest revenue.
- **Category dominance** – Technology leads in sales, but margin varies.
- **Unprofitable products** – Some sub‑categories (e.g., Tables) have high sales but negative profit due to discounts.
- **Profit margin** – Overall margin ~12.5%; low‑margin segments need review.

---

## 📁 Project Structure

SALES_ANALYSIS_PROJECT/
├── data/
│ └── superstore.csv # Raw data (Sample Superstore)
├── dashboard/
│ └── app.py # Main Streamlit application
├── notebooks/
│ └── eda_visualization.ipynb # Exploratory analysis
├── images/
│ └── dashboard.png # Dashboard screenshot
├── requirements.txt # Python dependencies
├── README.md # Project documentation
└── .gitignore # Ignored files

---

## ▶️ How to Run Locally

1. Clone the repository:
   ```bash
   git clone https://github.com/pexov26/DA_PROJECTS.git
   cd DA_PROJECTS/SALES_ANALYSIS_PROJECT