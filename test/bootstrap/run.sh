#!/bin/bash

# Set up all environment variables

export PROJECT_ID=$1

./app_engine.sh

# Set the BigQuery dataset ID and table ID
export DATASET_ID="test_bq_dataset1"
export TABLE_ID="test-bq-table"
./bigquery.sh # TODO: add region

./bigtable.sh

# Set Compute Instance and zone variables
export INSTANCE_NAME="github-action-runner"
export ZONE="us-west1-a"
./compute_instance.sh

# Set Compute Images and Snapshots variables
export IMAGE_NAME="image-1"
export SNAPSHOT_NAME="snapshot-1"
./compute_snapshots.sh
./compute_image.sh

export VPC_NETWORK_NAME="test-vpc"
export FILESTORE_INSTANCE_NAME="test-filestore1"
export FILESTORE_VOLUME_NAME="test_filestore1"
./filestore.sh

export POLICY_NAME="test-policy"
export TEST_NETWORK=$VPC_NETWORK_NAME
./dns.sh

export REGION="us-central1"
export FUNCTION_NAME="test-function-1"
export TOPIC_NAME="test-topic"
./functions.sh

export LOCATION="global"
export KEYRING_NAME="test-keyring"
export KEY_NAME="test-key1"
./kms.sh

# Set project and zone variables
export MACHINE_IMAGE_NAME="test-image-1"
export SOURCE_VM_NAME=$INSTANCE_NAME
./machine_images.sh

export MANAGED_ZONE_NAME="test-dns-zone90511"
./managed_zone.sh

export SUBSCRIPTION_NAME="test-subscription"
export TOPIC_NAME="test-topic"
./pubsub.sh

export REPO_NAME="test_source_repo"
./sourcerepos.sh

# Set SQL Variables
export SQL_INSTANCE_NAME="test-postresql"
export SQL_REGION="us-central1"
export TIER="db-f1-micro"
export DB_VERSION="POSTGRES_14"
export ROOT_PASSWORD="test"
export STORAGE_SIZE="10" # GB
./sql.sh

export BUCKET_NAME="gcp-scanner-test-bucket-$(cat /dev/urandom | tr -dc 'a-z0-9' | fold -w 8 | head -n 1)"
./storage.sh

./spanner.sh


