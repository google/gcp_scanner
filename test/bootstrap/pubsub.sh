#!/bin/bash

gcloud pubsub topics create $TOPIC_NAME

# Create the Pub/Sub subscription
gcloud pubsub subscriptions create $SUBSCRIPTION_NAME \
    --topic=$TOPIC_NAME \
    --ack-deadline=10 \
    --message-retention-duration=604800s \
    --enable-message-ordering \
    --expiration-period=never