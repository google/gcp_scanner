#!/bin/bash

gcloud services enable sqladmin.googleapis.com

# Create CloudSQL instance
gcloud sql instances create $SQL_INSTANCE_NAME \
  --database-version=$DB_VERSION \
  --tier=$TIER \
  --region=$SQL_REGION \
  --storage-size=$STORAGE_SIZE \
  --root-password=$ROOT_PASSWORD