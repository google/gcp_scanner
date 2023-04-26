#!/bin/bash

# Enable the AppEngine API
gcloud services enable appengine.googleapis.com

# Create a new AppEngine application in default region
gcloud app create

# Create an app.yaml file
echo "runtime: python38
entrypoint: python main.py
" > app.yaml

# Create a main.py file
echo "print('Hello, World!')" > main.py

# Deploy the application to App Engine
gcloud app deploy
