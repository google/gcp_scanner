#!/bin/bash

# gcloud services enable compute.googleapis.com

# create security policy named "test-security-policy"
gcloud compute security-policies create test-security-policy \
    --description "policy for external users"

# update default rule to deny all traffic (default rule has priority 2147483647)
gcloud compute security-policies rules update 2147483647 \
    --security-policy test-security-policy \
    --action "deny-404"