#!/bin/bash

BUCKET_NAME="gcp-scanner-test-bucket-$(cat /dev/urandom | tr -dc 'a-z0-9' | fold -w 8 | head -n 1)"

gsutil mb -l us-central1 gs://${BUCKET_NAME}
