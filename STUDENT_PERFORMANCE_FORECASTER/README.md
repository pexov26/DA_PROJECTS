

# 🎓 Student Performance Forecaster

[![Open in Streamlit](https://daprojects-nfg8dch3y5tobk2jxzqyqw.streamlit.app/)](#) 

*(**Note:** Replace the `#` above with your Streamlit Cloud link once deployed!)*

---

## 🚀 Project Overview

This project is an **interactive Machine Learning dashboard** built with Python and Streamlit. It acts as an end-to-end predictive engine, allowing users to input daily habits (study hours, sleep, phone usage) to instantly forecast student exam performance and visualize key metrics like productivity and focus.

The dashboard utilizes a modular architecture for clean, scalable code and is designed for seamless deployment.

---

## 📌 Key Features

| Feature | Description |
|---------|-------------|
| **Machine Learning Inference** | Uses a pre-trained Random Forest model to predict exam scores instantly based on user input. |
| **Dynamic UI Filters** | Interactive sidebar sliders for study hours, sleep hours, phone usage, and attendance. |
| **Live KPI Gauges** | Real-time dynamic calculation of Productivity and Focus scores using Plotly gauges. |
| **Deep-Dive Visualizations** | Analyzes the impact of AI tool usage on overall productivity across different student tiers. |
| **Eligibility Pipeline** | Automatically calculates and visualizes exam eligibility and fine requirements based on attendance. |
| **Modular Architecture** | Clean separation of concerns (UI, modeling, routing, and charts) for professional maintainability. |

---

## 🛠️ Tech Stack

- **Python** – Core logic and data processing
- **Pandas** – Data manipulation and aggregation
- **Scikit-Learn (Joblib)** – Machine Learning model training and inference
- **Plotly** – Interactive charts and gauge visualizations
- **Streamlit** – Dashboard framework and frontend UI

---

## 📈 Key Insights & Functionality

- **Habit Impact** – Instantly shows the correlation between screen time (phone usage) and a drop in forecasted exam scores.
- **Productivity vs. AI** – Visualizes how different tiers of students utilize AI tools and its direct impact on their productivity output.
- **Attendance Reality Check** – Clear, color-coded warnings and pipeline charts highlight students at risk of fines or exam ineligibility.
- **Performance Tiers** – Segments students into Toppers, Average, Below Average, and Poor to find trends in global performance.

---

## 📁 Project Structure

```text
STUDENT_PERFORMANCE_FORECASTER/
│
├── data/
│   └── ultimate_student_metrics_30k.csv  # Base dataset
├── models/
│   └── student_rf_model.pkl              # Compiled Random Forest model weights
├── notebooks/
│   ├── 01_EDA_and_CrossFiltering.ipynb   # Exploratory Data Analysis & visual mapping
│   └── 02_Model_Training_Pipeline.ipynb  # ML Training Pipeline & Hyperparameter tuning
├── src/
│   ├── charts_and_metrics.py             # Plotly visualization logic
│   ├── model_inference.py                # Model loading and prediction logic
│   └── ui_filters.py                     # Streamlit sidebar and UI inputs
│
├── app.py                                # Main Streamlit application runner
├── requirements.txt                      # Python dependencies
└── README.md                             # Project documentation
