#!/bin/bash

# Enable Cloud DNS API
gcloud services enable dns.googleapis.com

# Create policy
gcloud dns policies create $POLICY_NAME --enable-inbound-forwarding --description="A test policy" --networks=$TEST_NETWORK