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

+-----------------------------+
| NYC Taxi Trip Data |
| (Parquet) |
+-------------+---------------+
|
v
+-----------------------------+
| Taxi Zone Lookup |
| (CSV) |
+-------------+---------------+
|
v
+-----------------------------+
| NYC Weather Data |
| (JSON API) |
+-------------+---------------+
|
v
+---------------------------------------------------+

Apache PySpark
- Data Cleaning
- Invalid Trip Filtering
- Null Value Handling
- Feature Engineering
* Trip Duration
* Pickup Hour / Day / Weekend
* Weather Category
- Data Enrichment
* Borough & Zone Mapping
* Hourly Weather Join
+----------------------+----------------------------+

markdown
Copy code
                   |
                   v
+---------------------------------------------------+
| Parquet Staging Layer |
| - Cleaned and Enriched Data |
| - Optimized for Analytical Loading |
+----------------------+----------------------------+
|
v
+---------------------------------------------------+
| DuckDB Analytics Database |
| - Analytics-ready Tables |
| - High-performance SQL Queries |
| - Schema Validation & Inspection |
+----------------------+----------------------------+
|
v
+---------------------------------------------------+
| BI Dashboard |
| (Power BI / Tableau / Looker) |
| - Time-based Demand Analysis |
| - Weather Impact on Trips |
| - Weekday vs Weekend Trends |
+---------------------------------------------------+

pgsql
Copy code

### Architecture Flow Explanation

- **Data Ingestion Layer**  
  Raw data is ingested from Parquet (NYC taxi trips), CSV (taxi zone lookup), and a JSON-based weather API.

- **Processing & Transformation Layer**  
  Apache PySpark performs distributed transformations including data cleaning, validation, feature engineering, and enrichment with geographic and weather information.

- **Staging Layer**  
  Transformed datasets are written to a Parquet staging layer to ensure fault tolerance and efficient downstream loading.

- **Analytics Layer**  
  DuckDB ingests staged Parquet files and provides an analytics-ready database optimized for fast SQL queries and validation.

- **Visualization Layer**  
  BI tools connect directly to DuckDB to generate dashboards and analytical insights for decision-making.

This architecture demonstrates a **production-style ETL pipeline** that is scalable, modular, fault-tolerant, and suitable for both academic and real-world analytics use cases.
🔥 This version is FINAL:
