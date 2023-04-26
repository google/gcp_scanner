#!/bin/bash

gcloud services enable compute.googleapis.com

# create instance
gcloud compute instances create $INSTANCE_NAME \
  --zone=$ZONE \
  --machine-type=e2-micro \
  --boot-disk-size=10GB \
  --boot-disk-type=pd-standard \
  --image-family=debian-10 \
  --image-project=debian-cloud \
  --scopes=cloud-platform