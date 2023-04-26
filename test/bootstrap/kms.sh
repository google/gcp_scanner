#!/bin/bash

gcloud services enable cloudkms.googleapis.com

#printf "s3cr3t" | gcloud secrets create my-secret --data-file=- --replication-policy=user-managed --locations=global

# Create the key ring if it doesn't already exist
gcloud kms keyrings create $KEYRING_NAME --location $LOCATION || true

# Create the key if it doesn't already exist
gcloud kms keys create $KEY_NAME --location $LOCATION --keyring $KEYRING_NAME --purpose=encryption || true
