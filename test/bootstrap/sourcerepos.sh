#!/bin/bash

gcloud services enable sourcerepo.googleapis.com

# Create the repository
gcloud source repos create $REPO_NAME