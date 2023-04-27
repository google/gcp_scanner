#!/bin/bash

gcloud services enable compute.googleapis.com

# create instance
gcloud compute instances create $INSTANCE_NAME \
  --zone=$ZONE \
  --machine-type=e2-micro \
  --boot-disk-size=10GB \
  --boot-disk-type=pd-standard \
  --image-family=ubuntu-1804-lts \
  --image-project=ubuntu-os-cloud \
  --scopes=https://www.googleapis.com/auth/cloud-platform