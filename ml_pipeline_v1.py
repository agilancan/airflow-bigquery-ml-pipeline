from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.providers.google.cloud.operators.bigquery import BigQueryInsertJobOperator
from airflow.operators.python import PythonOperator
from airflow.operators.email import EmailOperator
import logging
import pandas as pd
from sklearn.linear_model import LinearRegression
import joblib
from google.cloud import storage
from google.cloud import bigquery

# GCS bucket for saving models and metrics (US bucket)
GCS_BUCKET = "us-composer-ml-bucket"

# Default DAG args
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
}

# DAG definition
dag = DAG(
    'ml_pipeline_us_bq',
    default_args=default_args,
    description='ML pipeline: BigQuery → train model → save metrics → log completion → send email',
    schedule_interval='0 0 * * 0',  # weekly
    start_date=days_ago(1),
    catchup=False,
)

# Task 1: Extract data from BigQuery
extract_query = """
SELECT *
FROM `airflow-bigquery-468916.ml_dataset_us.cycle_hire_features`
"""
data_task = BigQueryInsertJobOperator(
    task_id='extract_data',
    configuration={'query': {'query': extract_query, 'useLegacySql': False}},
    dag=dag,
)

# Task 2: Train model
def train_model(**kwargs):
    # Load data from BigQuery
    client = bigquery.Client()
    query = "SELECT * FROM `airflow-bigquery-468916.ml_dataset_us.cycle_hire_features`"
    df = client.query(query).to_dataframe()

    # Numerical features only
    X = df[['day_of_week', 'start_hour', 'start_station_id']]
    y = df['duration']

    # Train linear regression
    model = LinearRegression()
    model.fit(X, y)
    preds = model.predict(X)
    mse = ((preds - y) ** 2).mean()

    # Save model locally
    joblib.dump(model, "/tmp/linear_regression_model.joblib")

    # Upload model to GCS
    storage_client = storage.Client()
    bucket = storage_client.bucket(GCS_BUCKET)
    model_blob = bucket.blob("data/ml_models/linear_regression_model.joblib")
    model_blob.upload_from_filename("/tmp/linear_regression_model.joblib")

    # Save metrics to GCS
    metrics_blob = bucket.blob("data/ml_models/metrics.txt")
    metrics_blob.upload_from_string(f"Training MSE: {mse:.2f}")

    logging.info(f"Model trained. MSE: {mse:.2f}")
    return mse

training_task = PythonOperator(
    task_id='train_model',
    python_callable=train_model,
    provide_context=True,
    dag=dag,
)

# Task 3: Log completion
def log_completion(**kwargs):
    logging.info("🎉 Model training complete! Check GCS for saved model and metrics")

notification_task = PythonOperator(
    task_id='log_completion',
    python_callable=log_completion,
    dag=dag,
)

# Task 4: Email notification
email_task = EmailOperator(
    task_id='send_email',
    to='agilancan@gmail.com',
    subject='ML Pipeline Completed',
    html_content="🎉 The BigQuery → ML training pipeline has completed. Check GCS for the model and metrics.",
    dag=dag,
)

# Set dependencies
data_task >> training_task >> notification_task >> email_task
