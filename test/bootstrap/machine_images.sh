#!/bin/bash

gcloud compute machine-images create $MACHINE_IMAGE_NAME \
    --source-instance=$SOURCE_VM_NAME --source-instance-zone=$ZONE