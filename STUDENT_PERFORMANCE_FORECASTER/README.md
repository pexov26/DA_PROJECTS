# 🎓 Student Performance Forecaster

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://daprojects-nfg8dch3y5tobk2jxzqyqw.streamlit.app/)

**Live Demo:** [Click here to view the dashboard](https://daprojects-nfg8dch3y5tobk2jxzqyqw.streamlit.app/)

## 📌 Project Overview
The Student Performance Forecaster is an interactive, end-to-end Machine Learning web application designed to predict student exam scores based on daily lifestyle metrics. Built with a focus on clean UI and real-time inference, this dashboard allows educators and students to visualize how study habits, sleep schedules, and screen time impact academic success.

## 🚀 Key Features
* **Real-Time Predictions:** A custom-trained Random Forest Regressor instantly forecasts exam scores as user inputs change.
* **Performance Tiering:** Automatically categorizes predicted scores into actionable tiers (Toppers, Average, Below Average, Poor).
* **Eligibility Pipeline:** Flags attendance warning levels and estimates potential academic fines.
* **Interactive Dashboards:** Built-in exploratory data analysis (EDA) using Streamlit's native charting to visualize trends across 30,000 synthetic student records.

## 🛠️ Technical Stack
* **Language:** Python
* **Frontend UI:** Streamlit
* **Machine Learning:** Scikit-Learn (Random Forest Regressor)
* **Data Manipulation:** Pandas, NumPy
* **Model Serialization:** Joblib (Heavily compressed for fast cloud deployment)
* **Version Control & Deployment:** Git, GitHub, Streamlit Community Cloud

## 💻 Local Installation & Setup

If you want to run this project locally, follow these steps:

**1. Clone the Data Analytics monorepo:**
```bash
git clone [https://github.com/pexov26/DA_PROJECTS.git](https://github.com/pexov26/DA_PROJECTS.git)
cd DA_PROJECTS/STUDENT_PERFORMANCE_FORECASTER