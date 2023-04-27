#!/bin/bash


# Enable the BigQuery API
gcloud services enable bigquery.googleapis.com

# Create a new dataset
bq mk $DATASET_ID

# Create a new table within the dataset
bq mk --table $DATASET_ID.$TABLE_ID id:STRING,name:STRING

# Load data into the table
echo '{"id": "TestField", "name": "Test"}' | bq insert $DATASET_ID.$TABLE_ID