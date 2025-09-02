# Airflow & BigQuery ML Pipeline

[![Python](https://img.shields.io/badge/python-3.10-blue?logo=python&logoColor=white)](https://www.python.org/)  
[![Airflow](https://img.shields.io/badge/Apache%20Airflow-2.7-orange?logo=apache-airflow&logoColor=white)](https://airflow.apache.org/)  
[![Google Cloud](https://img.shields.io/badge/Google%20Cloud-4285F4?logo=googlecloud&logoColor=white)](https://cloud.google.com/)  

---

## Project Overview

This repository demonstrates a **production-grade ML pipeline** implemented with **Apache Airflow (Cloud Composer)** and **BigQuery**. The pipeline automates an end-to-end workflow for training a machine learning model on bike share trip data, persisting artifacts in **Google Cloud Storage (GCS)**, and notifying stakeholders upon completion.

The pipeline follows **industry best practices** for data persistence, reproducibility, logging, and modular DAG design.

---

## Key Features

- **Data Extraction from BigQuery:** Uses `BigQueryInsertJobOperator` for reliable, scalable SQL extraction.  
- **ML Model Training:** Linear Regression with `scikit-learn`, trained on features from bike-share trip data.  
- **Artifact Persistence in GCS:** Models and metrics uploaded for versioning and reproducibility.  
- **Logging & Notifications:** Cloud Logging messages and optional email via `EmailOperator`.  
- **Modular DAG Design:** Tasks are independent, with clear dependencies; easy to extend or scale.  

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

```
## Implementation Overview

The DAG consists of four main tasks:

1. **Data Extraction:** Uses `BigQueryInsertJobOperator` to query features and target from BigQuery.
2. **Model Training:** Linear Regression trained on selected numerical features (`day_of_week`, `start_hour`, `start_station_id`). Metrics (MSE) are logged and model artifacts are saved to GCS using `joblib`.
3. **Completion Logging:** Sends logs to Cloud Logging to track pipeline progress.
4. **Email Notification:** Optional email via `EmailOperator` informs stakeholders when training completes.

Tasks are chained to ensure sequential execution:  
`data_task >> training_task >> notification_task >> email_task`
## Implementation Overview

The DAG consists of four main tasks:

1. **Data Extraction:** Uses `BigQueryInsertJobOperator` to query features and target from BigQuery.
2. **Model Training:** Linear Regression trained on selected numerical features (`day_of_week`, `start_hour`, `start_station_id`). Metrics (MSE) are logged and model artifacts are saved to GCS using `joblib`.
3. **Completion Logging:** Sends logs to Cloud Logging to track pipeline progress.
4. **Email Notification:** Optional email via `EmailOperator` informs stakeholders when training completes.

Tasks are chained to ensure sequential execution:  
`data_task >> training_task >> notification_task >> email_task`

## Environment Setup

1. Cloud Composer 2 environment with service account roles:
   - `BigQuery Job User`
   - `Storage Object Admin`
2. Enable APIs:
   - BigQuery API
   - Cloud Composer API
3. Install Python dependencies via Composer PyPI:
   - `scikit-learn`
   - `pandas`
   - `joblib`

## Dataset & Model

- **Dataset:** `bigquery-public-data.london_bicycles.cycle_hire`
- **Prediction Target:** Trip duration
- **Features:** `day_of_week`, `start_hour`, `start_station_id`
- **Model:** Linear Regression (fast, interpretable, production-ready)

## Deployment & Demo

1. Upload DAG file to Composer DAGs bucket (`ml_pipeline_us_bq.py`).
2. Trigger manually in Airflow UI or schedule weekly.
3. Verify:
   - Model and metrics in GCS (`data/ml_models/linear_regression_model.joblib`)
   - Completion logs in Cloud Logging
   - Optional email notifications


## Production Considerations

- **Data Persistence:** BigQuery table ensures reproducibility and debugging.
- **Scalable Architecture:** DAG structured for large datasets; avoids Airflow XCom limits.
- **Monitoring & Notifications:** Cloud Logging and email alerts for pipeline visibility.
- **Modularity:** Tasks are independent; easy to extend for new models or datasets.


## Author

**Agilan Sivakumaran** – AI/ML & Cloud Engineering Enthusiast  
[Portfolio](https://agilan.online/) | [LinkedIn](https://www.linkedin.com/in/agilan-sivakumaran/) | [Email](mailto:agilan.sivakumaran@gmail.com)

## License

MIT License
