#!/bin/bash

# Set source disk URL
SOURCE_DISK_URL=$(gcloud compute instances describe $INSTANCE_NAME --zone=$ZONE --format='get(disks[0].source)')

# Set disk size in GB
DISK_SIZE_GB="10"

# Create snapshot using gcloud command
gcloud compute disks snapshot "${SOURCE_DISK_URL}" \
       --snapshot-names="${SNAPSHOT_NAME}" \
       --zone="${ZONE}" \
       --storage-location=us \
       --description="Snapshot of ${SOURCE_DISK_URL} with ${DISK_SIZE_GB} size."