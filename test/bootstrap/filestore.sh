#!/bin/bash

# Enable file.googleapis.com
gcloud services enable file.googleapis.com

# Enable subnet for filestore
gcloud compute networks create $VPC_NETWORK_NAME --subnet-mode=auto --bgp-routing-mode=regional

gcloud filestore instances create $FILESTORE_INSTANCE_NAME \
  --location=$ZONE \
  --tier=BASIC_HDD \
  --file-share=name=$FILESTORE_VOLUME_NAME,capacity=1024GB \
  --network=name=$VPC_NETWORK_NAME