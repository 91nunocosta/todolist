#!/bin/bash

printf "\n\n Create a user account \nS"
curl --location --request POST 'http://0.0.0.0:5000/accounts' \
--header 'Content-Type: application/json' \
--data-raw '{
    "username": "91nunocosta@gmail.com",
    "password": "unsercurepassword"
}'

printf "\n\n Login \n"
curl --location --request POST 'http://0.0.0.0:5000/login' \
--header 'Content-Type: application/json' \
--data-raw '{
    "username": "91nunocosta@gmail.com",
    "password": "unsercurepassword"
}'

printf "\n\n Create task \n"
curl --location --request POST 'http://0.0.0.0:5000/tasks' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiI5MW51bm9jb3N0YUBnbWFpbC5jb20iLCJpYXQiOjE2MTY2MTY5NjN9.tMQoy_6ROA_sxWR1exWVeRZZZFR4qvMbO2Szos_XIMI' \
--data-raw '{
    "summary": "Check that task can be created.",
    "done": false,
    "position": 1
}'

printf "\n\n List tasks \n"
curl --location --request GET 'http://0.0.0.0:5000/tasks' \
--header 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiI5MW51bm9jb3N0YUBnbWFpbC5jb20iLCJpYXQiOjE2MTY2MTY5NjN9.tMQoy_6ROA_sxWR1exWVeRZZZFR4qvMbO2Szos_XIMI'

printf "\n\n Update tasks \n"
curl --location --request PATCH 'http://0.0.0.0:5000/tasks/605b9e7052a0e74acae75fac' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiI5MW51bm9jb3N0YUBnbWFpbC5jb20iLCJpYXQiOjE2MTY2MTY5NjN9.tMQoy_6ROA_sxWR1exWVeRZZZFR4qvMbO2Szos_XIMI' \
--data-raw '{
    "done": true
}'

printf "\n\n Remove task \n"
curl --location --request DELETE 'http://0.0.0.0:5000/tasks/605b9e7052a0e74acae75fac' \
--header 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiI5MW51bm9jb3N0YUBnbWFpbC5jb20iLCJpYXQiOjE2MTY2MTY5NjN9.tMQoy_6ROA_sxWR1exWVeRZZZFR4qvMbO2Szos_XIMI'