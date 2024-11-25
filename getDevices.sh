#!/bin/bash

# GET /router/api/v1/user/devices HTTP/1.1
# Host: https://openapi.api.govee.com
# Content-Type: application/json
# Govee-API-Key: 929f506f-f061-4b3d-9cc1-117730797b7c

API_KEY="929f506f-f061-4b3d-9cc1-117730797b7c"

curl -X GET https://openapi.api.govee.com/router/api/v1/user/devices \
-H "Content-Type: application/json" \
-H "Govee-API-Key: $API_KEY"

