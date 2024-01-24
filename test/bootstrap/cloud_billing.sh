#!/bin/bash

gcloud services enable cloudbilling.googleapis.com

#### incase no billing account is associated with project, use steps below

# # install alpha component if not installed 
# gcloud components install alpha

# # list billing accounts associated with the current user, 
# gcloud alpha billing accounts list

# # link one of the billing accounts with project my-project
# gcloud alpha billing projects link my-project --billing-account 0X0X0X-0X0X0X-0X0X0X
