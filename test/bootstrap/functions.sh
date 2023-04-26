#!/bin/bash

# Enable the Cloud Functions API
gcloud services enable cloudfunctions.googleapis.com

# Create a new Cloud Function
gcloud functions deploy $FUNCTION_NAME \
  --region $REGION \
  --runtime python310 \
  --entry-point hello_world \
  --source test-function-1/
  --max-instances 30 \
  --memory 128MB \
  --ingress-settings ALL