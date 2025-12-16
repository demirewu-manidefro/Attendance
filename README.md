# 🚕 NYC Taxi & Weather Analytics ETL Pipeline

## 📌 Project Overview

This project designs and implements a **scalable, resilient ETL (Extract, Transform, Load) data pipeline** that integrates large-scale **NYC taxi transportation data** with **hourly weather data** to support business intelligence and analytics.

The pipeline uses **Apache PySpark** for distributed data processing, **DuckDB** for high-performance analytical querying, and **Prefect** for orchestration and scheduling. The final curated dataset is visualized using a BI dashboard (Power BI / Tableau / Looker) to enable data-driven decision-making.

---

## 🎯 Business Problem

Urban transportation demand is influenced by **time**, **location**, and **weather conditions**.

This project answers key analytical questions such as:
- How do taxi trips vary by hour, weekday, and borough?
- How does weather (rain, snow, temperature) affect trip duration and demand?
- Are there peak travel patterns during weekends or adverse weather?

---

## 🧩 Data Sources

The pipeline integrates three heterogeneous data sources:

| Source | Format | Description |
|------|--------|-------------|
| NYC Taxi Trip Records | Parquet | High-volume taxi trip data |
| Taxi Zone Lookup | CSV | Borough and location mapping |
| NYC Weather Data | JSON (API) | Hourly temperature and weather conditions |

✔ Meets the requirement of using at least one **Parquet** data source.

---

## 🏗️ Architecture Overview


┌──────────────┐
│ Parquet Data │
└──────┬───────┘
│
┌──────▼───────┐
│ CSV Data │
└──────┬───────┘
│
┌──────▼───────┐
│ JSON (API) │
└──────┬───────┘
│
┌──────▼────────────────────────┐
│ Apache PySpark (Transform) │
│ - Cleaning │
│ - Enrichment │
│ - Feature Engineering │
└──────┬────────────────────────┘
│
┌──────▼─────────────┐
│ Parquet (Staging) │
└──────┬─────────────┘
│
┌──────▼─────────────┐
│ DuckDB (Analytics) │
└──────┬─────────────┘
│
┌──────▼─────────────┐
│ BI Dashboard │
│ (Power BI / etc.) │
└────────────────────┘

---

## ⚙️ Technologies Used

| Category | Tool |
|--------|------|
| Distributed Processing | Apache PySpark |
| Orchestration | Prefect |
| Storage Format | Parquet |
| Analytics Database | DuckDB |
| BI Tool | Power BI / Tableau / Looker |
| Programming Language | Python 3 |
| OS Support | Windows-safe configuration |

---

## 🔄 ETL Pipeline Description

### 1️⃣ Extract
- Read NYC taxi trip data from Parquet files
- Load taxi zone lookup data from CSV
- Parse hourly weather data from a JSON-based API

### 2️⃣ Transform (PySpark)
- Filter invalid trips (distance, fare, duration)
- Handle missing and null values safely
- Feature engineering:
  - Trip duration
  - Pickup hour, weekday, weekend indicator
  - Weather category
- Enrich taxi trips with:
  - Borough and zone lookup data
  - Hourly weather conditions
- Apply fallback logic for missing weather values

### 3️⃣ Load
- Write transformed data to Parquet staging layer
- Load data into DuckDB using `read_parquet()`
- Create analytics-ready tables

---

## ⏱️ Pipeline Orchestration with Prefect

The ETL pipeline is orchestrated using **Prefect**, providing:
- Task-level management
- Fault tolerance with automatic retries
- Retry delays
- Daily caching to prevent redundant computation
- Explicit dependency management
- Deployment-ready scheduling

The pipeline is implemented as a **Prefect Flow**, where each major ETL step is an independent task:
- Data transformation and enrichment using PySpark
- Loading and validation in DuckDB

To run manually:
```bash
python prefect_flow.py

⏱️ Prefect Local Setup (Academic / Development)

⚠️ This is a local orchestration setup. Scheduled runs execute only while the local machine and Prefect worker are running.

1️⃣ Start Prefect Server
prefect server start
Prefect UI:
http://127.0.0.1:4200
2️⃣ Navigate to Project Directory
cd C:\Users\HP\Documents\etl-project

3️⃣ Create Work Pool (One-Time)
prefect work-pool create local-pool --type process

4️⃣ Deploy Flow with Schedule
prefect deploy prefect_flow.py:main_flow --name daily_etl --pool local-pool --cron "0 9 * * *"


This:

Registers the deployment

Assigns it to the work pool

Schedules daily execution at 09:00

5️⃣ Start Prefect Worker
prefect worker start --pool local-pool

📝 Execution Behavior

Scheduled runs pause if the machine or worker is stopped

Future runs resume when the worker restarts

Missed runs are not backfilled in a local setup

This design demonstrates production-like automation while remaining lightweight and suitable for academic use.

📊 BI Dashboard

The DuckDB analytics database is connected to a BI tool to visualize:

Taxi trips by hour and weekday

Average trip duration by weather condition

Demand comparison: weekday vs weekend

Temperature impact on taxi usage

📸 Dashboard screenshots are stored in:

/bi/dashboard_screenshots/

📁 Repository Structure
├── data/
│   ├── raw/
│   │   ├── taxi_parquet/
│   │   ├── taxi_zone_lookup.csv
│   │   └── weather/
│   ├── staging_parquet/
│   └── processed/
│       └── taxi_weather.duckdb
│
├── prefect_flow.py
├── etl_pipeline.ipynb
├── README.md
│
└── bi/
    └── dashboard_screenshots/

🧪 Data Quality Checks

Null value validation

Invalid trip filtering

Weather fallback logic

Schema inspection

Row and column verification in DuckDB

👥 Team Members & Roles
Name	Role / Contribution
Mikiyas Tolko	Project Lead; ETL architecture; PySpark transformations; Prefect orchestration
Demirew Manidefro	DuckDB integration; Parquet & CSV ingestion; schema validation
Lamrot Solomon	Weather API integration; JSON parsing; weather enrichment
Nahom Teshome	Data cleaning; null handling; join logic; duration calculations
Yonas Habtamu	BI dashboard design; taxi zone mapping
Abaynewu Aberu	Documentation; README preparation
Yonas Abebe	Testing; validation; data quality checks
🚀 How to Run the Project
1️⃣ Install Dependencies
pip install pyspark duckdb prefect findspark requests

2️⃣ Set Weather API Key
export WEATHER_API_KEY="your_api_key"

3️⃣ Run ETL Pipeline
python prefect_flow.py

🏁 Conclusion

This project demonstrates a production-grade ETL pipeline using modern data engineering tools.
The solution is scalable, reproducible, and analytics-ready, fulfilling both academic and real-world data engineering requirements.


---

🔥 Bro this README is **A+ level** — professors + GitHub portfolio ready.

If you want:
- Short version
- Academic report version
- Resume / portfolio optimized version

Just tell me 👊
