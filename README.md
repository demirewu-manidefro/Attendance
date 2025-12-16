# 🚕 NYC Taxi & Weather Analytics ETL Pipeline

## 📌 Project Overview
This project implements a scalable and resilient ETL (Extract, Transform, Load) pipeline that integrates NYC taxi trip data with hourly weather data to generate analytics-ready datasets for business intelligence reporting.

The pipeline uses Apache PySpark for distributed processing, DuckDB for analytics, and Prefect for orchestration. The final curated dataset is visualized using a BI dashboard (Power BI / Tableau / Looker).

---

## 🎯 Business Problem
Urban transportation demand is affected by time, location, and weather conditions.

This project answers:
- How do taxi trips vary by hour, weekday, and borough?
- How does weather (rain, snow, temperature) affect trip duration and demand?
- Are there peak travel patterns during weekends or bad weather?

---

## 🧩 Data Sources

| Source | Format | Description |
|------|--------|-------------|
| NYC Taxi Trip Records | Parquet | High-volume taxi trip data |
| Taxi Zone Lookup | CSV | Borough and location mapping |
| NYC Weather Data | JSON (API) | Hourly weather conditions |

✔ Includes at least one Parquet data source.

---

## 🏗️ Architecture Overview

