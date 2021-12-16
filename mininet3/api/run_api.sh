#!/usr/bin/env bash

# Helper to run the REST API:

uvicorn --reload --host 0.0.0.0 --port 80 mininet3.api.app:app
