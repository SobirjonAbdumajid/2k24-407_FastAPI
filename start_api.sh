#!/bin/bash

uvicorn app.server.app:create_app --reload --factory --host 0.0.0.0 --port 8000
