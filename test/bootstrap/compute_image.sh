#!/bin/bash

gcloud compute images create $IMAGE_NAME --source-snapshot=$SNAPSHOT_NAME