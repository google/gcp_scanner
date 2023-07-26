#!/bin/bash

# Enable datastore API
gcloud services enable datastore.googleapis.com

# Assign data to a variable in JSON format
data=$(
  cat <<EOF
[
    {"kind": "Person", "Person_id": "Lucy", "sex": "f", "age": 18},
    {"kind": "Pet", "Pet_id": "Cherie", "Person_id": "Lucy", "sex": "f", "type": "dog", "age": 7},
    {"kind": "Pet", "Pet_id": "Bubsy", "Person_id": "Lucy", "sex": "m", "type": "fish", "age": 3},
    {"kind": "Toy", "Toy_id": "tennis_ball", "Pet_id": "Cherie", "Person_id": "Lucy", "price": 0.99},
    {"kind": "Toy", "Toy_id": "castle", "Pet_id": "Bubsy", "Person_id": "Lucy", "price": 49.99},
    {"kind": "Toy", "Toy_id": "rope", "Pet_id": "Cherie", "Person_id": "Lucy", "price": 10.99}
]
EOF
)

# Run the gcloud datastore import command with the data
echo "${data}" | gcloud datastore import --kinds=Person,Pet,Toy --format=json
