#!/bin/bash

# Create the managed zone using the gcloud command
gcloud dns managed-zones create "$MANAGED_ZONE_NAME" \
  --project="$PROJECT_ID" \
  --dns-name="test-dns-name90511." \
  --description="Test DNS Zone Description" \
  --visibility="private" \
  --networks="projects/$PROJECT_ID/global/networks/test-vpc" \