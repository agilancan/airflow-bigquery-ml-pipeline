# Cloud Composer ML Pipeline: Automated Model Training & Notification  

[![Python](https://img.shields.io/badge/python-3.10-blue?logo=python&logoColor=white)](https://www.python.org/)  
[![Airflow](https://img.shields.io/badge/Apache%20Airflow-2.7-orange?logo=apache-airflow&logoColor=white)](https://airflow.apache.org/)  
[![Google Cloud](https://img.shields.io/badge/Google%20Cloud-4285F4?logo=googlecloud&logoColor=white)](https://cloud.google.com/)  

---

## Project Overview  

This repository demonstrates a **production-ready automated ML pipeline** built using **Google Cloud Composer** (managed Apache Airflow). The pipeline is designed to:  

1. **Extract data** from BigQuery.  
2. **Train a machine learning model** on the extracted dataset.  
3. **Persist the model and metrics** to Google Cloud Storage (GCS).  
4. **Notify stakeholders** via logging and optional email upon pipeline completion.  

The pipeline follows industry best practices for **data persistence, model reproducibility, and scalable orchestration**.

---

## Key Features  

- **Data Extraction:** Uses `BigQueryInsertJobOperator` to run parameterized SQL queries, extracting features and target variables from `bigquery-public-data.london_bicycles.cycle_hire`.  
- **ML Model Training:** Implements a simple, interpretable model using `scikit-learn` with persisted artifacts stored in GCS.  
- **Metrics Logging & Monitoring:** Captures evaluation metrics in JSON/CSV format and logs a completion summary in **Cloud Logging**.  
- **Email Notifications (Optional):** Configurable via Airflow `EmailOperator` for automated alerts.  
- **Scalable DAG Structure:** Tasks are modular, allowing seamless upgrades, additional data sources, or alternative ML models.  

---

## Architecture Diagram  

```text
+-----------------+       +----------------+       +---------------------+
| BigQuery Source | --->  | Airflow DAG    | --->  | GCS (Model & Metrics) |
|                 |       | Task: Data     |       |                     |
| cycle_hire table|       | Extraction     |       |                     |
+-----------------+       +----------------+       +---------------------+
                                   |
                                   v
                           +----------------+
                           | Task: Model    |
                           | Training       |
                           +----------------+
                                   |
                                   v
                           +----------------+
                           | Task: Notification |
                           | Logging & Email   |
                           +----------------+
